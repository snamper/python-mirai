from pydantic import BaseModel
from . import ExternalEvent, ExternalEventTypes as EventType
from ..group import Permission, Group, Member
from ..friend import Friend
import typing as T

class BotOnlineEvent(ExternalEvent):
    type: EventType = EventType.BotOnlineEvent
    qq: int

class BotOfflineEventActive(ExternalEvent):
    type: EventType = EventType.BotOfflineEventActive
    qq: int

class BotOfflineEventForce(ExternalEvent):
    type: EventType = EventType.BotOfflineEventForce
    qq: int

class BotOfflineEventDropped(ExternalEvent):
    type: EventType = EventType.BotOfflineEventDropped
    qq: int

class BotReloginEvent(ExternalEvent):
    type: EventType = EventType.BotReloginEvent
    qq: int

class BotGroupPermissionChangeEvent(ExternalEvent):
    type: EventType = EventType.BotGroupPermissionChangeEvent
    origin: Permission
    new: Permission
    group: Group

class BotMuteEvent(ExternalEvent):
    type: EventType = EventType.BotMuteEvent
    durationSeconds: int
    operator: T.Optional[Member]

class BotUnmuteEvent(ExternalEvent):
    type: EventType = EventType.BotUnmuteEvent
    operator: T.Optional[Member]

class BotJoinGroupEvent(ExternalEvent):
    type: EventType = EventType.BotJoinGroupEvent
    group: Group

class GroupNameChangeEvent(ExternalEvent):
    type: EventType = EventType.GroupNameChangeEvent
    origin: str
    new: str
    group: Group
    isByBot: bool

class GroupEntranceAnnouncementChangeEvent(ExternalEvent):
    type: EventType = EventType.GroupEntranceAnnouncementChangeEvent
    origin: str
    new: str
    group: Group
    operator: T.Optional[Member]

class GroupMuteAllEvent(ExternalEvent):
    type: EventType = EventType.GroupMuteAllEvent
    origin: bool
    new: bool
    group: Group
    operator: T.Optional[Member]

class GroupAllowAnonymousChatEvent(ExternalEvent):
    type: EventType = EventType.GroupAllowAnonymousChatEvent
    origin: bool
    new: bool
    group: Group
    operator: T.Optional[Member]

class GroupAllowConfessTalkEvent(ExternalEvent):
    type: EventType = EventType.GroupAllowAnonymousChatEvent
    origin: bool
    new: bool
    group: Group
    isByBot: bool

class GroupAllowMemberInviteEvent(ExternalEvent):
    type: EventType = EventType.GroupAllowMemberInviteEvent
    origin: bool
    new: bool
    group: Group
    operator: T.Optional[Member]

class MemberJoinEvent(ExternalEvent):
    type: EventType = EventType.MemberJoinEvent
    member: Member

class MemberLeaveEventKick(ExternalEvent):
    type: EventType = EventType.MemberLeaveEventKick
    member: Member
    operator: T.Optional[Member]

class MemberLeaveEventQuit(ExternalEvent):
    type: EventType = EventType.MemberLeaveEventQuit
    member: Member

class MemberCardChangeEvent(ExternalEvent):
    type: EventType = EventType.MemberCardChangeEvent
    origin: str
    new: str
    member: Member
    operator: T.Optional[Member]

class MemberSpecialTitleChangeEvent(ExternalEvent):
    type: EventType = EventType.MemberSpecialTitleChangeEvent
    origin: str
    new: str
    member: Member

class MemberPermissionChangeEvent(ExternalEvent):
    type: EventType = EventType.MemberPermissionChangeEvent
    origin: str
    new: str
    member: Member

class MemberMuteEvent(ExternalEvent):
    type: EventType = EventType.MemberMuteEvent
    durationSeconds: int
    member: Member
    operator: T.Optional[Member]

class MemberUnmuteEvent(ExternalEvent):
    type: EventType = EventType.MemberUnmuteEvent
    member: Member
    operator: T.Optional[Member]