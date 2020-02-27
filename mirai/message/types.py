import typing as T
from enum import Enum
from .base import MessageComponentTypes
from mirai.friend import Friend
from mirai.group import Group, Member
from pydantic import BaseModel
from .chain import MessageChain

class MessageItemType(Enum):
    FriendMessage = "FriendMessage"
    GroupMessage = "GroupMessage"
    BotMessage = "BotMessage"

class FriendMessage(BaseModel):
    type: MessageItemType = "FriendMessage"
    messageChain: T.Optional[MessageChain]
    sender: Friend

class GroupMessage(BaseModel):
    type: MessageItemType = "GroupMessage"
    messageChain: T.Optional[MessageChain]
    sender: Member

class BotMessage(BaseModel):
    type: MessageItemType = 'BotMessage'
    messageId: int

MessageTypes = {
    "GroupMessage": GroupMessage,
    "FriendMessage": FriendMessage
}