import typing as T
from urllib import parse
from .network import fetch, session
from .protocol import MiraiProtocol
from .group import Group
from .friend import Friend
from .message.types import FriendMessage, GroupMessage, MessageTypes, MessageItemType
from .event import InternalEvent, ExternalEvent, ExternalEventTypes, ExternalEvents
import asyncio
from threading import Thread, Lock
from contextvars import ContextVar
import random
import traceback
from mirai.logger import message as MessageLogger, event as EventLogger
from mirai.misc import printer

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
      self.cached_groups = {group.id: group for group in await super().groupList()}
    if self.cache_options['friends']:
      self.cached_friends = {friend.id: friend for friend in await super().friendList()}

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
    async def connect():
      with self.shared_lock:
        await asyncio.wait([
          self.event_runner(lambda: self.exit_signal, self.event_stacks),
          self.message_polling(lambda: self.exit_signal, self.event_stacks)
        ])
    def inline_warpper(loop: asyncio.AbstractEventLoop):
      asyncio.set_event_loop(loop)
      loop.create_task(connect())
      loop.run_forever()
    self.async_runtime = Thread(target=inline_warpper, args=(self.another_loop,), daemon=True)

  def start_event_runtime(self):
    self.async_runtime.start()

  async def __aenter__(self) -> "Session":
    #self.polling_runtime.__enter__() # 短轮询运行时启动
    #self.event_runtime.__enter__()
    #self.shared_runtime.__enter__()
    self.setting_event_runtime()
    self.start_event_runtime()
    return await self.enable_session()

  async def __aexit__(self, exc_type, exc, tb):
    await self.close_session(ignoreError=True)
    await session.close()

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
            name=item.__class__.__name__ if isinstance(item, ( # normal class
                  UnexceptedException,
                  ExternalEvent,
                )) else item.__name__ if item in [ # pydantic model
                  GroupMessage,
                  FriendMessage
                ] else item.name if isinstance(item, ( # enum
                  ExternalEvents
                )) else item,
            body=result[message_index]
          )
        )

  def receiver(self, event_name, 
      addon_condition: T.Optional[
        T.Callable[[T.Union[FriendMessage, GroupMessage]], bool]
      ] = None):
    def receiver_warpper(
      func: T.Callable[[T.Union[FriendMessage, GroupMessage], "Session"], T.Awaitable[T.Any]]
    ):
      if event_name not in self.event:
        self.event[event_name] = [{addon_condition: func}]
      else:
        self.event[event_name].append({addon_condition: func})
      return func
    return receiver_warpper

  async def event_runner(self, exit_signal_status, queue: asyncio.Queue):
    from .prototypes.context import (
      MessageContextBody, EventContextBody, # body
    )
    from .context import message as MessageContext, event as EventContext
    while not exit_signal_status():
      event_context: InternalEvent
      try:
        event_context: InternalEvent = await asyncio.wait_for(queue.get(), 3)
      except asyncio.exceptions.TimeoutError:
        if exit_signal_status():
          break
        else:
          continue

      if event_context.name in self.getRegisteredEventNames:
        for event in list(self.event.values())\
              [self.getRegisteredEventNames.index(event_context.name)]:
          if event: # 判断是否有注册.
            for pre_condition, run_body in event.items():
              try:
                condition_result = (not pre_condition) or (pre_condition(event_context.body))
              except Exception as e:
                if event_context.name != "UnexceptedException":
                  #print("error: by pre:", event_context.name)
                  EventLogger.error(f"a error threw by {event_context.name}'s condition.")
                  await queue.put(InternalEvent(
                    name="UnexceptedException",
                    body=UnexceptedException(
                      error=e,
                      event=event_context,
                      session=self
                    )
                  ))
                else:
                  traceback.print_exc()
                continue
              if condition_result:
                MessageContext.set(None)
                EventContext.set(None)

                context_body: T.Union[MessageContextBody, EventContextBody]
                internal_context_object: \
                  T.Union[MessageContext, EventContext]
                if hasattr(ExternalEvents, event_context.name):
                  EventLogger.info(f"[Event::{event_context.name}] is handling...")
                  internal_context_object = EventContext
                  context_body = EventContextBody(
                    event=event_context.body,
                    session=self
                  )
                elif event_context.name in MessageTypes:
                  MessageLogger.info(f"[Message::{event_context.name}] is handling...")
                  internal_context_object = MessageContext
                  context_body = MessageContextBody(
                    message=event_context.body,
                    session=self
                  )
                else:
                  EventLogger.warning("a unknown event is handling...")
                  context_body = event_context.body
                internal_context_object.set(context_body) # 设置完毕.
                try:
                  await run_body(context_body)
                except Exception as e:
                  if event_context.name != "UnexceptedException":
                    EventLogger.error(f"a error(Exception::{e.__class__.__name__}) threw by {event_context.name}'s processing body.")
                    await queue.put(InternalEvent(
                      name="UnexceptedException",
                      body=UnexceptedException(
                        error=e,
                        event=event_context,
                        session=self
                      )
                    ))
                    traceback.print_exc()
                  else:
                    traceback.print_exc()

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

  async def joinMainThread(self):
    while self.shared_lock.locked():
      await asyncio.sleep(0.01)
    else:
      return True

  def exception_handler(self, exception_class=None, addon_condition=None):
    return self.receiver(
      "UnexceptedException", 
      lambda context: \
          True \
        if not exception_class else \
          type(context.error) == exception_class and (
            addon_condition(context) \
              if addon_condition else \
            True
          )
    )


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

  async def getGroup(self, target: int) -> T.Optional[Group]:
    return self.cached_groups.get(target)
  
  async def getFriend(self, target: int) -> T.Optional[Friend]:
    return self.cached_friends.get(target)

  @property
  def getRegisteredEventNames(self):
    return [i.__name__ if isinstance(i, ( # normal class
      UnexceptedException,
      ExternalEvent,
    )) else i.__name__ if i in [ # pydantic model
      GroupMessage,
      FriendMessage
    ] else i.name if isinstance(i, ( # enum
      ExternalEvents
    )) else i for i in self.event.keys()]


from .event.builtins import UnexceptedException