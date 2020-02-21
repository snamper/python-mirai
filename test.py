import asyncio
from mirai import Session, MiraiProtocol
from mirai import MessageChain, Plain, FriendMessage, GroupMessage, At
from mirai.message.components import Unknown
from mirai.misc import printer
from pathlib import Path
from pprint import pprint
from typing import Union

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver("GroupMessage", lambda m: m.sender.group.id == 655057127)
        async def _(
                message: GroupMessage,
                session_: Session, protocol: MiraiProtocol):
            if isinstance(message, GroupMessage):
                await protocol.sendGroupMessage(
                    message.sender.group, 
                    (   
                        Plain(text="meow."), 
                        At(
                            target=message.sender.id,
                            display=f"@{message.sender.memberName}"
                        )
                    )
                )

        #print(session.event)
        while True:
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                session.close_session()

asyncio.run(main())