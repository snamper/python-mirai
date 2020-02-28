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
                await session.sendGroupMessage(group, [
                    printer(await Image.fromFileSystem("./photo_2020-02-28_16-55-34.jpg" , "group"))
                ])
                print("meow!")

        print(session.enabled)
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()