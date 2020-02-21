import asyncio
from typing import Union

from mirai.message.components import At, Plain
from mirai.message.types import FriendMessage, GroupMessage
from mirai.message.chain import MessageChain
from mirai.protocol import MiraiProtocol
from mirai.session import Session

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver("GroupMessage", lambda m: m.sender.group.id == 655057127)
        async def _(context):
            if isinstance(context.message, GroupMessage):
                print(f"[{context.message.sender.group.id}][{context.message.sender.id}]:", context.message.messageChain.toString())

        #print(session.event)
        while True:
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                break

asyncio.run(main())
