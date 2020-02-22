## Mirai Framework for Python

#### 这是什么?
以 OICQ(QQ) 协议驱动的高性能机器人开发框架 [Mirai](https://github.com/mamoe/mirai) 的 Python 接口, 通过其提供的 `HTTP API` 与无头客户端(`Mirai`)交互.

#### 一些Demo

``` python
import asyncio

from mirai.message.components import At, Plain
from mirai.message.types import FriendMessage, GroupMessage
from mirai.event.builtins import UnexceptedException
from mirai.session import Session
from mirai.context import MessageContextBody

from pprint import pprint
from devtools import debug

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver("GroupMessage", lambda m: m.sender.group.id == 655057127) # 上下文支持
        async def normal_handle(context):
            if isinstance(context.message, GroupMessage): # 提供了基本的API
                context: MessageContextBody

                print(f"[{context.message.sender.group.id}][{context.message.sender.id}]:", context.message.messageChain.toString()) # toString方法的调用 在这之后会进行优化
                if context.message.messageChain.toString().startswith("/raiseAnother"):
                    raise ValueError("fa")
                elif context.message.messageChain.toString().startswith("/raise"):
                    raise Exception("test")
                elif context.message.messageChain.toString().startswith("/meow"):
                    await context.session.sendGroupMessage(
                        context.event.body.sender.group.id,
                        [Plain(text="meow."), At(target=context.message.sender.id)] # 
                    )

        @session.exception_handler(Exception)
        @session.exception_handler(ValueError)
        async def exception_handle(context: UnexceptedException):
            await context.session.sendGroupMessage(
                context.event.body.sender.group.id,
                Plain(text=f"{context.error.__class__.__name__}: {context.error.args}")
            )
        
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()
```