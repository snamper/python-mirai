from collections import namedtuple
from typing import Any
from enum import Enum
from pydantic import BaseModel

# 内部事件实现.
InternalEvent = namedtuple("Event", ("name", "body"))

class ExternalEventTypes(Enum):
    BotOnlineEvent = "BotOnlineEvent"
    BotOfflineEventActive = "BotOfflineEventActive"
    BotOfflineEventForce = "BotOfflineEventForce"
    BotOfflineEventDropped = "BotOfflineEventDropped"
    BotReloginEvent = "BotReloginEvent"
    BotGroupPermissionChangeEvent = "BotGroupPermissionChangeEvent"
    BotMuteEvent = "BotMuteEvent"
    BotUnmuteEvent = "BotUnmuteEvent"
    BotJoinGroupEvent = "BotJoinGroupEvent"

    GroupNameChangeEvent = "GroupNameChangeEvent"
    GroupEntranceAnnouncementChangeEvent = "GroupEntranceAnnouncementChangeEvent"
    GroupMuteAllEvent = "GroupMuteAllEvent"

    # 群设置被修改事件
    GroupAllowAnonymousChatEvent = "GroupAllowAnonymousChatEvent" # 群设置 是否允许匿名聊天 被修改
    GroupAllowConfessTalkEvent = "GroupAllowConfessTalkEvent" # 坦白说
    GroupAllowMemberInviteEvent = "GroupAllowMemberInviteEvent" # 邀请进群

    # 群事件(被 Bot 监听到的, 为"被动事件", 其中 Bot 身份为第三方.)
    MemberJoinEvent = "MemberJoinEvent"
    MemberLeaveEventKick = "MemberLeaveEventKick"
    MemberLeaveEventQuit = "MemberLeaveEventQuit"
    MemberCardChangeEvent = "MemberCardChangeEvent"
    MemberSpecialTitleChangeEvent = "MemberSpecialTitleChangeEvent"
    MemberPermissionChangeEvent = "MemberPermissionChangeEvent"
    MemberMuteEvent = "MemberMuteEvent"
    MemberUnmuteEvent = "MemberUnmuteEvent"

    # python-mirai 自己提供的事件
    UnexceptedException = "UnexceptedException"

class ExternalEvent(BaseModel):
    type: ExternalEventTypes

from . import external

class ExternalEvents(Enum):
    BotOnlineEvent = external.BotOnlineEvent
    BotOfflineEventActive = external.BotOfflineEventActive
    BotOfflineEventForce = external.BotOfflineEventForce
    BotOfflineEventDropped = external.BotOfflineEventDropped
    BotReloginEvent = external.BotReloginEvent
    BotGroupPermissionChangeEvent = external.BotGroupPermissionChangeEvent
    BotMuteEvent = external.BotMuteEvent
    BotUnmuteEvent = external.BotUnmuteEvent
    BotJoinGroupEvent = external.BotJoinGroupEvent

    GroupNameChangeEvent = external.GroupNameChangeEvent
    GroupEntranceAnnouncementChangeEvent = external.GroupEntranceAnnouncementChangeEvent
    GroupMuteAllEvent = external.GroupMuteAllEvent

    # 群设置被修改事件
    GroupAllowAnonymousChatEvent = external.GroupAllowAnonymousChatEvent # 群设置 是否允许匿名聊天 被修改
    GroupAllowConfessTalkEvent = external.GroupAllowConfessTalkEvent # 坦白说
    GroupAllowMemberInviteEvent = external.GroupAllowMemberInviteEvent # 邀请进群

    # 群事件(被 Bot 监听到的, 为被动事件, 其中 Bot 身份为第三方.)
    MemberJoinEvent = external.MemberJoinEvent
    MemberLeaveEventKick = external.MemberLeaveEventKick
    MemberLeaveEventQuit = external.MemberLeaveEventQuit
    MemberCardChangeEvent = external.MemberCardChangeEvent
    MemberSpecialTitleChangeEvent = external.MemberSpecialTitleChangeEvent
    MemberPermissionChangeEvent = external.MemberPermissionChangeEvent
    MemberMuteEvent = external.MemberMuteEvent
    MemberUnmuteEvent = external.MemberUnmuteEvent

