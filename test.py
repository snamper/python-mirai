import asyncio
from mirai import Session, Plain, Friend, BotMuteEvent
from devtools import debug

authKey = "213we355gdfbaerg"
qq = 208924405

async def main():
    async with Session(f"mirai://localhost:8070/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)
        @session.receiver("FriendMessage")
        async def event_friendmessage(session: Session, sender: Friend):
            await session.sendFriendMessage(
                sender.id,
                [Plain(text="Hello, world!")]
            )

        @session.receiver("BotMuteEvent")
        async def event_BotMuteEvent(event: BotMuteEvent):
            debug(event)

        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()