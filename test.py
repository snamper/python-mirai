import asyncio
from mirai import Session, MiraiProtocol
from mirai import MessageChain, PlainMessage, FriendMessage, GroupMessage, AtMessage
from pathlib import Path
from pprint import pprint
from typing import Union

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver("FriendMessage")
        @session.receiver("GroupMessage", lambda m: m.sender.id == 1846913566)
        async def _(
                message: Union[FriendMessage, GroupMessage],
                session_: Session, protocol: MiraiProtocol):
            if isinstance(message, GroupMessage):
                await protocol.sendGroupMessage(
                    message.sender.group, 
                    PlainMessage(text="meow.") + AtMessage(target=1846913566)
                )

        #print(session.event)
        while True:
            try:
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                session.close_session()

asyncio.run(main())