import asyncio
from mirai import Session, Plain, Friend, BotMuteEvent, BotUnmuteEvent, Group, Member, MessageChain, Image, Depend
from devtools import debug
from mirai.misc import printer

authKey = "213we355gdfbaerg"
qq = 208924405

async def test2():
    print(2)

async def test(session: Session, q = Depend(test2)):
    print(session)
    return 1

async def main():
    async with Session(f"mirai://localhost:8070/?authKey={authKey}&qq={qq}") as session:
        @session.receiver("GroupMessage")
        async def event_gm(session: Session, message: MessageChain, group: Group):
            if message.toString().startswith("/image"):
                await session.sendGroupMessage(group, [
                    Image.fromFileSystem("E:\\Image\\00C49FCD-D8D9-4966-B2FC-F18F6220485E.jpg"),
                    Plain(text="??")
                ])
            
        @session.receiver("FriendMessage")
        async def event_gm(session: Session, message: MessageChain, friend: Friend):
            if message.toString().startswith("/image"):
                await session.sendFriendMessage(friend, [
                    Image.fromFileSystem("E:\\Image\\00C49FCD-D8D9-4966-B2FC-F18F6220485E.jpg"),
                    Plain(text="??")
                ])
                
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()