import asyncio
import contextlib
import copy
import inspect
import json
import random
import traceback
import typing as T
from contextvars import ContextVar
from functools import partial
from threading import Lock, Thread
from urllib import parse

from mirai.misc import printer, raiser

from .depend import Depend
from .event import ExternalEvent, ExternalEventTypes, InternalEvent
from .event.external.enums import ExternalEvents
from .event.message import components
from .event.message.types import (
    FriendMessage, GroupMessage, MessageItemType, MessageTypes)
from .friend import Friend
from .group import Group, Member
from .logger import Event as EventLogger
from .logger import Session as SessionLogger
from .network import fetch, session
from .protocol import MiraiProtocol

class Session(MiraiProtocol):
  cache_options: T.Dict[str, bool] = {}

  cached_groups: T.Dict[int, Group] = {}
  cached_friends: T.Dict[int, Friend] = {}

  enabled: bool = False

  event_stacks: asyncio.Queue
  event = {}

  async_runtime: Thread = None
  another_loop: asyncio.AbstractEventLoop
  exit_signal: bool = False

  def __init__(self, 
    url: T.Optional[str] = None, # 

    host: T.Optional[str] = None,
    port: T.Optional[int] = None,
    authKey: T.Optional[str] = None,
    qq: T.Optional[int] = None,

    cache_groups: T.Optional[bool] = True,
    cache_friends: T.Optional[bool] = True
  ):
    if url:
      urlinfo = parse.urlparse(url)
      if urlinfo:
        query_info = parse.parse_qs(urlinfo.query)
        if all((
          urlinfo.scheme == "mirai",
          urlinfo.path == "/",

          "authKey" in query_info and query_info["authKey"],
          "qq" in query_info and query_info["qq"]
        )):
          # 确认过了, 无问题
          authKey = query_info["authKey"][0]

          self.baseurl = f"http://{urlinfo.netloc}"
          self.auth_key = authKey
          self.qq = query_info["qq"][0]
        else:
          raise ValueError("invaild url: wrong format")
      else:
        raise ValueError("invaild url")
    else:
      if all([host, port, authKey, qq]): 
        self.baseurl = f"http://{host}:{port}"
        self.auth_key = authKey
        self.qq = qq
      else:
        raise ValueError("invaild arguments")

    self.cache_options['groups'] = cache_groups
    self.cache_options['friends'] = cache_friends

    self.shared_lock = Lock()
    self.another_loop = asyncio.new_event_loop()
    self.event_stacks = asyncio.Queue(loop=self.another_loop)

  async def enable_session(self) -> "Session":
    auth_response = await super().auth()
    if all([
      "code" in auth_response and auth_response['code'] == 0,
      "session" in auth_response and auth_response['session'] or\
        "msg" in auth_response and auth_response['msg'] # polyfill
    ]):
      if "msg" in auth_response and auth_response['msg']:
        self.session_key = auth_response['msg']
      else:
        self.session_key = auth_response['session']

      await super().verify()
    else:
      if "code" in auth_response and auth_response['code'] == 1:
        raise ValueError("invaild authKey")
      else:
        raise ValueError('invaild args: unknown response')
    
    if self.cache_options['groups']:
      await self.cacheBotGroups()
    if self.cache_options['friends']:
      await self.cacheBotFriends()

    self.enabled = True
    return self

  @classmethod
  async def start(cls,
    url: T.Optional[str] = None,

    host: T.Optional[str] = None,
    port: T.Optional[int] = None,
    authKey: T.Optional[str] = None,
    qq: T.Optional[int] = None,

    cache_groups: T.Optional[bool] = True,
    cache_friends: T.Optional[bool] = True
  ):
    self = cls(url, host, port, authKey, qq, cache_groups, cache_friends)
    return await self.enable_session()

  def setting_event_runtime(self):
    def inline_warpper(loop: asyncio.AbstractEventLoop):
      asyncio.set_event_loop(loop)
      loop.create_task(self.get_tasks())
      loop.run_forever()
    self.async_runtime = Thread(target=inline_warpper, args=(self.another_loop,), daemon=True)

  def start_event_runtime(self):
    self.async_runtime.start()

  async def __aenter__(self) -> "Session":
    await self.enable_session()
    self.setting_event_runtime()
    self.start_event_runtime()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.close_session(ignoreError=True)
    await session.close()

  async def get_tasks(self):
    "用于为外部的事件循环注入 event_runner 和 message_polling"
    with self.shared_lock:
      await asyncio.wait([
        self.event_runner(lambda: self.exit_signal, self.event_stacks),
        self.message_polling(lambda: self.exit_signal, self.event_stacks)
      ])

  async def message_polling(self, exit_signal_status, queue, count=10):
    while not exit_signal_status():
      await asyncio.sleep(0.5)

      result: T.List[T.Union[FriendMessage, GroupMessage, ExternalEvent]] = \
        await super().fetchMessage(count)
      last_length = len(result)
      latest_result = []
      while True:
        if last_length == count:
          latest_result = await super().fetchMessage(count)
          last_length = len(latest_result)
          result += latest_result
          continue
        break
      
      # 开始处理
      # 事件系统实际上就是"lambda", 指定事件名称(like. GroupMessage), 然后lambda判断.
      # @event.receiver("GroupMessage", lambda info: info.......)
      for message_index in range(len(result)):
        item = result[message_index]
        await queue.put(
          InternalEvent(
            name=self.getEventCurrentName(type(item)),
            body=item
          )
        )

  def receiver(self, event_name, 
      addon_condition: T.Optional[
        T.Callable[[T.Union[FriendMessage, GroupMessage]], bool]
      ] = None,
      dependencies: T.List[Depend] = [],
      use_middlewares: T.List[T.Callable] = []
    ):
    def receiver_warpper(
      func: T.Callable[[T.Union[FriendMessage, GroupMessage], "Session"], T.Awaitable[T.Any]]
    ):
      if not inspect.iscoroutinefunction(func):
        raise TypeError("event body must be a coroutine function.")

      protocol = {addon_condition: {
        "func": func,
        "dependencies": dependencies,
        "middlewares": use_middlewares
      }}  
      
      if event_name not in self.event:
        self.event[event_name] = [protocol]
      else:
        self.event[event_name].append(protocol)
      return func
    return receiver_warpper

  async def throw_exception_event(self, event_context, queue, exception):
    from .event.builtins import UnexpectedException
    if event_context.name != "UnexpectedException":
      #print("error: by pre:", event_context.name)
      await queue.put(InternalEvent(
        name="UnexpectedException",
        body=UnexpectedException(
          error=exception,
          event=event_context,
          session=self
        )
      ))
      EventLogger.error(f"threw a exception by {event_context.name}, Exception: {exception}")
      traceback.print_exc()
    else:
      EventLogger.critical(f"threw a exception by {event_context.name}, Exception: {exception}, it's a exception handler.")

  async def argument_compiler(self, func, event_context):
    annotations_mapping = self.get_annotations_mapping()
    signature_mapping = self.signature_getter(func)
    translated_mapping = { # 执行主体
      k: annotations_mapping[v](
        event_context
      )\
      for k, v in func.__annotations__.items()\
        if \
          k != "return" and \
          k not in signature_mapping # 嗯...你设了什么default? 放你过去.
    }
    return translated_mapping

  def signature_getter(self, func):
    "获取函数的默认值列表"
    return {k: v.default \
      for k, v in dict(inspect.signature(func).parameters).items() \
        if v.default != inspect._empty}

  def signature_checker(self, func):
    signature_mapping = self.signature_getter(func)
    for i in signature_mapping.values():
      if not isinstance(i, Depend):
        raise TypeError("you must use a Depend to patch the default value.")

  async def signature_checkout(self, func, event_context, queue):
    signature_mapping = self.signature_getter(func)
    return {
      k: await self.main_entrance(
        v.func,
        event_context,
        queue
      ) for k, v in signature_mapping.items()
    }

  async def main_entrance(self, run_body, event_context, queue):
    if isinstance(run_body, dict):
      callable_target = run_body['func']
      for depend in run_body['dependencies']:
        await self.main_entrance(
          {"func": depend.func.__call__, "middlewares": depend.middlewares},
          event_context, queue
        )
    else:
      callable_target = run_body.__call__

    translated_mapping = {
      **(await self.argument_compiler(
        callable_target,
        event_context
      )),
      **(await self.signature_checkout(
        callable_target,
        event_context,
        queue
      ))
    }

    try:
      if isinstance(run_body, dict):
        middlewares = run_body.get("middlewares")
        if middlewares:
          async_middlewares = []
          normal_middlewares = []

          for middleware in middlewares:
            if all([
              hasattr(middleware, "__aenter__"),
              hasattr(middleware, "__aexit__")
            ]):
              async_middlewares.append(middleware)
            elif all([
              hasattr(middleware, "__enter__"),
              hasattr(middleware, "__exit__")
            ]):
              normal_middlewares.append(middleware)
            else:
              SessionLogger.error(f"threw a exception by {event_context.name}, no currect context error.")
              raise AttributeError("no a currect context object.")

          async with contextlib.AsyncExitStack() as async_stack:
            for async_middleware in async_middlewares:
              SessionLogger.debug(f"a event called {event_context.name}, enter a currect async context.")
              await async_stack.enter_async_context(async_middleware)
            with contextlib.ExitStack() as normal_stack:
              for normal_middleware in normal_middlewares:
                SessionLogger.debug(f"a event called {event_context.name}, enter a currect context.")
                normal_stack.enter_context(normal_middleware)
              if inspect.iscoroutinefunction(callable_target):
                return await callable_target(**translated_mapping)
              else:
                return callable_target(**translated_mapping)

      if inspect.iscoroutinefunction(callable_target):
        return await callable_target(**translated_mapping)
      else:
        return callable_target(**translated_mapping)
    except (NameError, TypeError) as e:
      EventLogger.error(f"threw a exception by {event_context.name}, it's about Annotations Checker, please report to developer.")
      traceback.print_exc()
    except Exception as e:
      EventLogger.error(f"threw a exception by {event_context.name}, and it's {e}")
      await self.throw_exception_event(event_context, queue, e)
      
  async def event_runner(self, exit_signal_status, queue: asyncio.Queue):
    while not exit_signal_status():
      event_context: InternalEvent
      try:
        event_context: T.NamedTuple[InternalEvent] = await asyncio.wait_for(queue.get(), 3)
      except asyncio.TimeoutError:
        if exit_signal_status():
          break
        else:
          continue

      if event_context.name in self.registeredEventNames:
        for event in list(self.event.values())\
              [self.registeredEventNames.index(event_context.name)]:
          if event: # 判断是否是 []/{}
            for pre_condition, run_body in event.items():
              try:
                condition_result = (not pre_condition) or (pre_condition(event_context.body))
              except Exception as e:
                self.throw_exception_event(event_context, queue, e)
                continue
              if condition_result:
                EventLogger.info(f"handling a event: {event_context.name}")

                asyncio.create_task(self.main_entrance(
                  run_body,
                  event_context, queue
                ))

  async def close_session(self, ignoreError=False):
    if self.enabled:
      self.exit_signal = True
      while self.shared_lock.locked():
        pass
      else:
        self.another_loop.call_soon_threadsafe(self.another_loop.stop)
        self.async_runtime.join()
      await super().release()
      self.enabled = False
    else:
      if not ignoreError:
        raise ConnectionAbortedError("session closed.")

  async def stop_event_runtime(self):
    if not self.async_runtime:
      raise ConnectionError("runtime stoped.")
    self.exit_signal = True
    while self.shared_lock.locked():
      pass
    else:
      self.another_loop.call_soon_threadsafe(self.another_loop.stop)
      self.async_runtime.join()

  def getRestraintMapping(self):
    from .event.message import MessageChain
    def warpper(name, event_context):
      return name == event_context.name
    return {
      Session: lambda k: True,
      GroupMessage: lambda k: k.name == "GroupMessage",
      FriendMessage: lambda k: k.name =="FriendMessage",
      MessageChain: lambda k: k.name in MessageTypes,
      components.Source: lambda k: k.name in MessageTypes,
      Group: lambda k: k.name == "GroupMessage",
      Friend: lambda k: k.name =="FriendMessage",
      Member: lambda k: k.name == "GroupMessage",
      "Sender": lambda k: k.name in MessageTypes,
      "Type": lambda k: k.name,
      **({
        event_class.value: partial(warpper, copy.copy(event_name))
        for event_name, event_class in \
          ExternalEvents.__members__.items()
      })
    }

  def checkEventBodyAnnotations(self):
    event_bodys: T.Dict[T.Callable, T.List[str]] = {}
    for event_name in self.event:
      event_body_list = sum([list(i.values()) for i in self.event[event_name]], [])
      for i in event_body_list:
        if not event_bodys.get(i['func']):
          event_bodys[i['func']] = [event_name]
        else:
          event_bodys[i['func']].append(event_name)
    
    restraint_mapping = self.getRestraintMapping()
    
    for func in event_bodys:
      whileList = self.signature_getter(func)
      for param_name, func_item in func.__annotations__.items():
        if param_name not in whileList:
          for event_name in event_bodys[func]:
            try:
              if not (restraint_mapping[func_item](
                  type("checkMockType", (object,), {
                    "name": event_name
                  })
                )
              ):
                raise ValueError(f"error in annotations checker: {func}.{func_item}: {event_name}")
            except KeyError:
              raise ValueError(f"error in annotations checker: {func}.{func_item} is invaild.")
            except ValueError:
              raise

  def checkEventDependencies(self):
    for event_name, event_bodys in self.event.items():
      for i in event_bodys:
        value = list(i.values())[0]
        for depend in value['dependencies']:
          if type(depend) != Depend:
            raise TypeError(f"error in dependencies checker: {value['func']}: {event_name}")

  async def joinMainThread(self):
    self.checkEventDependencies()
    self.checkEventBodyAnnotations()
    SessionLogger.info("session ready.")
    while self.shared_lock:
      await asyncio.sleep(0.01)
    else:
      return

  def exception_handler(self, exception_class=None, addon_condition=None):
    return self.receiver(
      "UnexpectedException", 
      lambda context: \
          True \
        if not exception_class else \
          type(context.error) == exception_class and (
            addon_condition(context) \
              if addon_condition else \
            True
          )
    )

  def gen_event_anno(self):
    IReturn = {}
    for event_name, event_class in ExternalEvents.__members__.items():
      def warpper(name, event_context):
        if name != event_context.name:
          raise ValueError("cannot look up a non-listened event.")
        return event_context.body
      IReturn[event_class.value] = partial(warpper, copy.copy(event_name))
    return IReturn

  def get_annotations_mapping(self):
    from .event.message import MessageChain
    return {
      Session: lambda k: self,
      GroupMessage: lambda k: k.body \
        if k.name == "GroupMessage" else\
          raiser(ValueError("you cannot setting a unbind argument.")),
      FriendMessage: lambda k: k.body \
        if k.name == "FriendMessage" else\
          raiser(ValueError("you cannot setting a unbind argument.")),
      MessageChain: lambda k: k.body.messageChain\
        if k.name in MessageTypes else\
          raiser(ValueError("MessageChain is not enable in this type of event.")),
      components.Source: lambda k: k.body.messageChain.getSource()\
        if k.name in MessageTypes else\
          raiser(TypeError("Source is not enable in this type of event.")),
      Group: lambda k: k.body.sender.group\
        if k.name == "GroupMessage" else\
          raiser(ValueError("Group is not enable in this type of event.")),
      Friend: lambda k: k.body.sender\
        if k.name == "FriendMessage" else\
          raiser(ValueError("Friend is not enable in this type of event.")),
      Member: lambda k: k.body.sender\
        if k.name == "GroupMessage" else\
          raiser(ValueError("Group is not enable in this type of event.")),
      "Sender": lambda k: k.body.sender\
        if k.name in MessageTypes else\
          raiser(ValueError("Sender is not enable in this type of event.")),
      "Type": lambda k: k.name,
      **self.gen_event_anno()
    }

  async def refreshBotGroupsCache(self) -> T.Dict[int, Group]:
    self.cached_groups = {group.id: group for group in await super().groupList()}
    return self.cached_groups
  
  async def refreshBotFriendsCache(self) -> T.Dict[int, Friend]:
    self.cached_friends = {friend.id: friend for friend in await super().friendList()}
    return self.cached_friends

  async def cacheBotGroups(self):
    if not self.cache_options['groups']:
      self.cached_groups = {group.id: group for group in await super().groupList()}

  async def cacheBotFriends(self):
    if not self.cache_options['friends']:
      self.cached_friends = {friend.id: friend for friend in await super().friendList()}

  def getGroup(self, target: int) -> T.Optional[Group]:
    return self.cached_groups.get(target)
  
  def getFriend(self, target: int) -> T.Optional[Friend]:
    return self.cached_friends.get(target)

  def getEventCurrentName(self, event_value):
    from .event.builtins import UnexpectedException
    if inspect.isclass(event_value) and issubclass(event_value, ExternalEvent): # subclass
      return event_value.__name__
    elif isinstance(event_value, ( # normal class
      UnexpectedException,
      GroupMessage,
      FriendMessage
    )):
      return event_value.__name__
    elif event_value in [ # message
      GroupMessage,
      FriendMessage
    ]:
      return event_value.__name__
    elif isinstance(event_value, ( # enum
      MessageItemType,
      ExternalEvents
    )):
      return event_value.name
    else:
      return event_value

  @property
  def registeredEventNames(self):
    return [self.getEventCurrentName(i) for i in self.event.keys()]
