import asyncio

from mirai.message.components import At, Plain, Face, Image
from mirai.face import QQFaces
from mirai.message.types import FriendMessage, GroupMessage
from mirai.event.builtins import UnexceptedException
from mirai.session import Session
from mirai.prototypes.context import MessageContextBody
from mirai.misc import printer, ImageType
import mirai.exceptions
from mirai.event import ExternalEvents
from mirai.event import external

from pprint import pprint
from devtools import debug
import traceback

async def main():
    authKey = "213we355gdfbaerg"
    qq = 208924405

    async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
        print(session.enabled)

        @session.receiver(GroupMessage, lambda m: m.sender.group.id == 655057127)
        async def normal_handle(context):
            if isinstance(context.message, GroupMessage):
                context: MessageContextBody

                print(f"[{context.message.sender.group.id}][{context.message.sender.id}]:", context.message.messageChain.toString())
                #debug(context)
                if context.message.messageChain.toString().startswith("/raiseAnother"):
                    raise ValueError("fa")
                elif context.message.messageChain.toString().startswith("/raise"):
                    raise Exception("test")
                elif context.message.messageChain.toString().startswith("/test-at"):
                    await context.session.sendGroupMessage(
                        context.message.sender.group.id,
                        [
                            At(target=context.message.sender.id),
                            Plain(text="meow"),
                            Face(faceId=QQFaces["jingkong"])
                        ]
                    )
                elif context.message.messageChain.toString().startswith("/test-localimage"):
                    await context.session.sendGroupMessage(
                        context.message.sender.group.id,
                        [
                            await Image.fromFileSystem("2019-05-04_15.52.03.png", session, ImageType.Group),
                            Plain(text="faq")
                        ]
                    )
                elif context.message.messageChain.toString().startswith("/muteMe"):
                    await context.session.mute(
                        context.message.sender.group.id,
                        context.message.sender.id,
                        60
                    )
                    await asyncio.sleep(5)
                    await context.session.unmute(
                        context.message.sender.group.id,
                        context.message.sender.id
                    )
                elif context.message.messageChain.toString().startswith("/replyMe"):
                    await context.session.sendQuoteMessage(
                       context.message.messageChain[0].id,
                       [Plain(text="??")]
                    )
                if Image in [type(i) for i in context.message.messageChain]:
                    pass

        @session.receiver(ExternalEvents.MemberMuteEvent)
        #@session.receiver(ExternalEvents.BotMuteEvent)
        #@session.receiver("BotMuteEvent")
        @session.receiver(external.BotMuteEvent)
        async def _(context):
            debug(context)

        @session.exception_handler(Exception)
        async def exception_handle(context: UnexceptedException):
            debug(context)
        
        await session.joinMainThread()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    exit()
