import asyncio
from mirai import Session, Plain, Friend, BotMuteEvent, BotUnmuteEvent, Group, Member, MessageChain, Image
from devtools import debug
from mirai.misc import printer

authKey = "213we355gdfbaerg"
qq = 208924405

async def main():
    async with Session(f"mirai://localhost:8070/?authKey={authKey}&qq={qq}") as session:
        @session.receiver("GroupMessage")
        async def event_gm(session: Session, message: MessageChain, group: Group):
            if message.toString().startswith("/image"):
                print("meow!")
                await session.sendGroupMessage(group, [
                    await Image.fromFileSystem("./00C49FCD-D8D9-4966-B2FC-F18F6220485E.jpg" , "group"),
                    Plain(text="??")
                ])
            
        @session.receiver("FriendMessage")
        async def event_gm(session: Session, message: MessageChain, friend: Friend):
            if message.toString().startswith("/image"):
                print("meow!")
                await asyncio.sleep(10)
                await session.sendFriendMessage(friend, [
                    #await Image.fromFileSystem("./photo_2020-02-28_16-55-34.jpg" , "friend"),
                    Plain(text="??")
                ])
                
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()