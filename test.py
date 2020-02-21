import asyncio
from typing import Union

from mirai import (At, FriendMessage, GroupMessage, MessageChain,
                   MiraiProtocol, Plain, Session)


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
                break

asyncio.run(main())
