import asyncio

from mirai.message.components import At, Plain, Face
from mirai.face import QQFaces
from mirai.message.types import FriendMessage, GroupMessage
from mirai.event.builtins import UnexceptedException
from mirai.session import Session
from mirai.context import MessageContextBody
from mirai.misc import printer
import mirai.exceptions

from pprint import pprint
from devtools import debug
import traceback

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver("GroupMessage", lambda m: m.sender.group.id == 655057127)
        async def normal_handle(context):
            if isinstance(context.message, GroupMessage):
                context: MessageContextBody

                print(f"[{context.message.sender.group.id}][{context.message.sender.id}]:", context.message.messageChain.toString())
                if context.message.messageChain.toString().startswith("/raiseAnother"):
                    raise ValueError("fa")
                elif context.message.messageChain.toString().startswith("/raise"):
                    raise Exception("test")
                elif context.message.messageChain.toString().startswith("/test-at"):
                    print(await context.session.sendGroupMessage(
                        context.message.sender.group.id,
                        [
                            printer(At(target=context.message.sender.id)),
                            Plain(text="meow"),
                            Face(faceId=QQFaces["jingkong"])
                        ]
                    ))

        @session.exception_handler(mirai.exceptions.NetworkError)
        async def exception_handle(context: UnexceptedException):
            debug(context)
        
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()
