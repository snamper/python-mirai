import typing as T
from enum import Enum
from .chain import MessageChain
from . import MessageComponentTypes
from mirai.friend import Friend
from mirai.group import Group, Member
from pydantic import BaseModel

class MessageItemType(Enum):
    FriendMessage = "FriendMessage"
    GroupMessage = "GroupMessage"

class FriendMessage(BaseModel):
    type: MessageItemType = "FriendMessage"
    message_id: int
    messageChain: T.Optional[MessageChain]
    sender: Friend

class GroupMessage(BaseModel):
    type: MessageItemType = "GroupMessage"
    messageChain: T.Optional[MessageChain]
    sender: Member

MessageTypes = {
    "GroupMessage": GroupMessage,
    "FriendMessage": FriendMessage
}