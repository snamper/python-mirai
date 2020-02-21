import re
import typing as T
from datetime import timedelta
from pathlib import Path
from uuid import UUID
import json

from mirai.message.types import FriendMessage, GroupMessage, MessageTypes

from mirai.event import ExternalEvent, ExternalEvents
from mirai.friend import Friend
from mirai.group import Group, GroupSetting, Member, MemberChangeableSetting
from mirai.image import Image
from mirai.message.chain import MessageChain
from mirai.misc import ImageRegex, ImageType, assertOperatorSuccess, raiser, printer
from mirai.network import fetch
from mirai.message.base import BaseMessageComponent
#from .context import MessageContext
import threading

class MiraiProtocol:
    qq: int
    baseurl: str
    session_key: str
    auth_key: str

    async def auth(self):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/auth", {
                "authKey": self.auth_key
            }
        ), raise_exception=True, return_as_is=True)

    async def verify(self):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/verify", {
                "sessionKey": self.session_key,
                "qq": self.qq
            }
        ), raise_exception=True, return_as_is=True)

    async def release(self):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/release", {
                "sessionKey": self.session_key,
                "qq": self.qq
            }
        ), raise_exception=True)

    async def sendFriendMessage(self,
            target: T.Union[Friend, int],
            message: T.Union[
                MessageChain,
                BaseMessageComponent,
                T.List[BaseMessageComponent]
            ]
    ):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/sendFriendMessage", {
                "sessionKey": self.session_key,
                "target": target,
                "messageChain": json.loads(message.json() \
                    if isinstance(message, MessageChain) else \
                        [json.loads(message.json())]) \
                    if isinstance(message, BaseMessageComponent) else \
                        [json.loads(i.json()) for i in message]
                    if isinstance(message, (tuple, list)) else \
                        raiser(ValueError("invaild message(s)."))
            }
        ), raise_exception=True)
    
    async def sendGroupMessage(self, target: T.Union[Group, int], message: MessageChain):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/sendGroupMessage", {
                "sessionKey": self.session_key,
                "target": target if isinstance(target, int) else \
                    target.id if isinstance(target, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "messageChain": json.loads(message.json() \
                    if isinstance(message, MessageChain) else \
                        [json.loads(message.json())]) \
                    if isinstance(message, BaseMessageComponent) else \
                        [json.loads(i.json()) for i in message]
                    if isinstance(message, (tuple, list)) else \
                        raiser(ValueError("invaild message(s)."))
            }
        ), raise_exception=True)

    async def groupList(self) -> T.List[Group]:
        return [Group.parse_obj(group_info) \
            for group_info in await fetch.http_get(f"{self.baseurl}/groupList", {
                "sessionKey": self.session_key
            })
        ]

    async def friendList(self) -> T.List[Friend]:
        return [Friend.parse_obj(friend_info) \
            for friend_info in await fetch.http_get(f"{self.baseurl}/friendList", {
                "sessionKey": self.session_key
            })
        ]

    async def memberList(self, target: int) -> T.List[Member]:
        return [Member.parse_obj(member_info) \
            for member_info in await fetch.http_get(f"{self.baseurl}/memberList", {
                "sessionKey": self.session_key,
                "target": target
            })
        ]

    async def groupMemberNumber(self, target: int) -> int:
        return len(await self.memberList(target)) + 1

    async def uploadImage(self, type: T.Union[str, ImageType], imagePath: T.Union[Path, str]):
        if isinstance(imagePath, str):
            imagePath = Path(imagePath)

        if not imagePath.exists():
            raise FileNotFoundError("invaild image path.")

        regex = ImageRegex[type if isinstance(type, str) else type.value]
        uuid_string = re.search(regex, 
            await fetch.upload(f"{self.baseurl}/uploadImage", imagePath, {
                "sessionKey": self.session_key,
                "type": type if isinstance(type, str) else type.value
            }
        ))

        return Image(
            id=UUID(uuid_string.string[slice(*uuid_string.span())]),
            suffix=imagePath.suffix[1:]
        )

    async def fetchMessage(self, count: int) -> T.List[T.Union[FriendMessage, GroupMessage, ExternalEvent]]:
        result = assertOperatorSuccess(
            await fetch.http_get(f"{self.baseurl}/fetchMessage", {
                "sessionKey": self.session_key,
                "count": count
            }
        ), raise_exception=True, return_as_is=True)
        for index in range(len(result)):
            if result[index]['type'] in MessageTypes:
                if 'messageChain' in result[index]:
                    result[index]['messageChain'] = MessageChain.custom_parse(result[index]['messageChain'])
                result[index] = \
                    MessageTypes[result[index]['type']].parse_obj(result[index])
            elif hasattr(ExternalEvents, result[index]['type']):
                result[index] = \
                    ExternalEvents[result[index]['type']].value.parse_obj(result[index])
        return result

    async def muteAll(self, target: T.Union[Group, int]) -> bool:
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/muteAll", {
                "sessionKey": self.session_key,
                "target": target if isinstance(target, int) else \
                    target.id if isinstance(target, Group) else \
                        raiser(ValueError("invaild target as group."))
            }
        ), raise_exception=True)
        
    async def unmuteAll(self, target: T.Union[Group, int]) -> bool:
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/unmuteAll", {
                "sessionKey": self.session_key,
                "target": target if isinstance(target, int) else \
                    target.id if isinstance(target, Group) else \
                        raiser(ValueError("invaild target as group."))
            }
        ), raise_exception=True)
    
    async def memberInfo(self,
        group: T.Union[Group, int],
        member: T.Union[Member, int],
    ):
        return assertOperatorSuccess(
            await fetch.http_get(f"{self.baseurl}/groupConfig", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "memberId": member if isinstance(member, int) else \
                    member.id if isinstance(member, Member) else \
                        raiser(ValueError("invaild target as member."))
            }
        ), raise_exception=True, return_as_is=True)

    async def botMemberInfo(self,
        group: T.Union[Group, int]
    ):
        return await self.memberInfo(group, self.qq)

    async def changeMemberInfo(self,
        group: T.Union[Group, int],
        member: T.Union[Member, int],
        setting: MemberChangeableSetting
    ) -> bool:
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/memberInfo", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "memberId": member if isinstance(member, int) else \
                    member.id if isinstance(member, Member) else \
                        raiser(ValueError("invaild target as member.")),
                "info": json.loads(setting.json())
            }
        ), raise_exception=True)

    async def groupConfig(self, group: T.Union[Group, int]) -> GroupSetting:
        return GroupSetting.parse_obj(
            await fetch.http_get(f"{self.baseurl}/groupConfig", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group."))
            })
        )

    async def changeGroupConfig(self,
        group: T.Union[Group, int],
        config: GroupSetting
    ) -> bool:
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/groupConfig", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "config": json.loads(json.loads(config.json()))
            }
        ), raise_exception=True)

    async def mute(self,
        group: T.Union[Group, int],
        member: T.Union[Member, int],
        time: T.Union[timedelta, int]
    ):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/mute", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "memberId": member if isinstance(member, int) else \
                    member.id if isinstance(member, Member) else \
                        raiser(ValueError("invaild target as member.")),
                "time": time if isinstance(time, int) else \
                        int(time.total_seconds()) \
                            if timedelta(days=30) >= time >= timedelta(minutes=1) \
                        else \
                            int(timedelta(days=30).total_seconds()) \
                                if timedelta(days=30) >= time else \
                            int(timedelta(minutes=1).total_seconds()) \
                                if time <= timedelta(minutes=1) else \
                            raiser(ValueError("invaild time."))
                    if isinstance(time, timedelta) else raiser(ValueError("invaild time."))
            }
        ), raise_exception=True)

    async def unmute(self,
        group: T.Union[Group, int],
        member: T.Union[Member, int]
    ):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/unmute", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "memberId": member if isinstance(member, int) else \
                    member.id if isinstance(member, Member) else \
                        raiser(ValueError("invaild target as member.")),
            }
        ), raise_exception=True)

    async def kick(self,
        group: T.Union[Group, int],
        member: T.Union[Member, int],
        kickMessage: T.Optional[str] = None
    ):
        return assertOperatorSuccess(
            await fetch.http_post(f"{self.baseurl}/kick", {
                "sessionKey": self.session_key,
                "target": group if isinstance(group, int) else \
                    group.id if isinstance(group, Group) else \
                        raiser(ValueError("invaild target as group.")),
                "memberId": member if isinstance(member, int) else \
                    member.id if isinstance(member, Member) else \
                        raiser(ValueError("invaild target as member.")),
                **({
                    "msg": kickMessage
                } if kickMessage else {})
            }
        ), raise_exception=True)

from mirai.message.components import MessageComponents