## Mirai Framework for Python

#### 这是什么?
以 OICQ(QQ) 协议驱动的高性能机器人开发框架 [Mirai](https://github.com/mamoe/mirai) 的 Python 接口, 通过其提供的 `HTTP API` 与无头客户端(`Mirai`)交互.

#### 一些Demo

``` python
import asyncio
from mirai import Session, MiraiProtocol
from mirai import MessageChain, PlainMessage, FriendMessage, GroupMessage, AtMessage
from typing import Union

async def main():
    authKey: str = "your authKey"
    qq: int = "your qq"

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled) # 判断 session 是否已经可用

        @session.receiver("FriendMessage")
        @session.receiver("GroupMessage", lambda m: m.sender.group == 234532452345) # 已经实现一些上下文应用
        async def event_handler(
                message: Union[FriendMessage, GroupMessage],
                session_: Session, protocol: MiraiProtocol):
            if isinstance(message, GroupMessage):
                await protocol.sendGroupMessage(
                    message.sender.group, 
                    PlainMessage(text="meow.") + AtMessage(target=message.sender.id)
                )

        while True: # Session 不会帮你堵塞主线程, 自行实现一个吧.
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                session.close_session()

asyncio.run(main())
```