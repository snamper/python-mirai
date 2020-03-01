from . import *
from enum import Enum

class ExternalEvents(Enum):
    BotOnlineEvent = BotOnlineEvent
    BotOfflineEventActive = BotOfflineEventActive
    BotOfflineEventForce = BotOfflineEventForce
    BotOfflineEventDropped = BotOfflineEventDropped
    BotReloginEvent = BotReloginEvent
    BotGroupPermissionChangeEvent = BotGroupPermissionChangeEvent
    BotMuteEvent = BotMuteEvent
    BotUnmuteEvent = BotUnmuteEvent
    BotJoinGroupEvent = BotJoinGroupEvent

    GroupNameChangeEvent = GroupNameChangeEvent
    GroupEntranceAnnouncementChangeEvent = GroupEntranceAnnouncementChangeEvent
    GroupMuteAllEvent = GroupMuteAllEvent

    # 群设置被修改事件
    GroupAllowAnonymousChatEvent = GroupAllowAnonymousChatEvent # 群设置 是否允许匿名聊天 被修改
    GroupAllowConfessTalkEvent = GroupAllowConfessTalkEvent # 坦白说
    GroupAllowMemberInviteEvent = GroupAllowMemberInviteEvent # 邀请进群

    # 群事件(被 Bot 监听到的, 为被动事件, 其中 Bot 身份为第三方.)
    MemberJoinEvent = MemberJoinEvent
    MemberLeaveEventKick = MemberLeaveEventKick
    MemberLeaveEventQuit = MemberLeaveEventQuit
    MemberCardChangeEvent = MemberCardChangeEvent
    MemberSpecialTitleChangeEvent = MemberSpecialTitleChangeEvent
    MemberPermissionChangeEvent = MemberPermissionChangeEvent
    MemberMuteEvent = MemberMuteEvent
    MemberUnmuteEvent = MemberUnmuteEvent

