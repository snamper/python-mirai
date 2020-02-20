from enum import Enum
from dataclasses import dataclass

class Permission(Enum):
    Member = "MEMBER"
    Administrator = "ADMINISTRATOR"
    Owner = "OWNER"

class Group:
    id: int
    name: str
    botPermission: Permission

    @classmethod
    def parser(cls, info_map):
        group = cls()
        group.id = info_map['id']
        group.name = info_map['name']
        group.botPermission = Permission(info_map['permission'])
        return group

    def __repr__(self):
        return f"<Group id={self.id} name='{self.name}' permission={self.botPermission.name}>"

class Member:
    id: int
    memberName: str
    memberPermission: Permission
    group: Group

    @classmethod
    def parser(cls, info_map):
        member = cls()
        member.id = info_map['id']
        member.memberName = info_map['memberName']
        member.memberPermission = info_map['permission']
        member.group = Group.parser(info_map['group'])
        return member

    def __repr__(self):
        return f"<GroupMember id={self.id} group={self.group} permission={self.memberPermission} group={self.group.id}>"

@dataclass(init=True)
class MemberChangeableSetting:
    name: str
    specialTitle: str

    def render(self):
        return {
            "name": self.name,
            "specialTitle": self.specialTitle
        }

    def modify(self, **kwargs):
        for i in ("name", "kwargs"):
            if i in kwargs:
                setattr(self, i, kwargs[i])
        return self

@dataclass(init=True)
class GroupSetting:
    name: str
    announcement: str
    confessTalk: bool
    allowMemberInvite: bool
    autoApprove: bool
    anonymousChat: bool

    def render(self):
        return {
            "name": self.name,
            "announcement": self.announcement,
            "confessTalk": self.confessTalk,
            "allowMemberInvite": self.allowMemberInvite,
            "autoApprove": self.autoApprove,
            "anonymousChat": self.anonymousChat
        }

    @classmethod
    def parser(cls, setting: dict) -> "GroupSetting":
        return cls(
            name=setting['name'],
            announcement=setting["announcement"],
            confessTalk=setting["confessTalk"],
            allowMemberInvite=setting['allowMemberInvite'],
            autoApprove=setting["autoApprove"],
            anonymousChat=setting['anonymousChat']
        )

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