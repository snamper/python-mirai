from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel
from PIL import Image
from mirai.network import session
from io import BytesIO

class Permission(Enum):
    Member = "MEMBER"
    Administrator = "ADMINISTRATOR"
    Owner = "OWNER"

class Group(BaseModel):
    id: int
    name: str
    permission: Permission

    def __repr__(self):
        return f"<Group id={self.id} name='{self.name}' permission={self.permission.name}>"

    def getAvatarUrl(self) -> str:
        return f'https://p.qlogo.cn/gh/{self.id}/{self.id}_1/140'

    async def getAvatarAsPillowImage(self) -> Image.Image:
        async with session.get(self.getAvatarUrl()) as response:
            return Image.open(BytesIO(await response.read()))

class Member(BaseModel):
    id: int
    memberName: str
    permission: Permission
    group: Group

    def __repr__(self):
        return f"<GroupMember id={self.id} group={self.group} permission={self.permission} group={self.group.id}>"

    def getAvatarUrl(self) -> str:
        return f'http://q4.qlogo.cn/g?b=qq&nk={self.id}&s=140'

    async def getAvatarAsPillowImage(self) -> Image.Image:
        async with session.get(self.getAvatarUrl()) as response:
            return Image.open(BytesIO(await response.read()))

class MemberChangeableSetting(BaseModel):
    name: str
    specialTitle: str

    def modify(self, **kwargs):
        for i in ("name", "kwargs"):
            if i in kwargs:
                setattr(self, i, kwargs[i])
        return self

class GroupSetting(BaseModel):
    name: str
    announcement: str
    confessTalk: bool
    allowMemberInvite: bool
    autoApprove: bool
    anonymousChat: bool

    def modify(self, **kwargs):
        for i in ("name",
            "announcement",
            "confessTalk",
            "allowMemberInvite",
            "autoApprove",
            "anonymousChat"
        ):
            if i in kwargs:
                setattr(self, i, kwargs[i])
        return self