import typing as T
from enum import Enum
from mirai.message import MessageChain, UsableMessages
from mirai.friend import Friend
from mirai.group import Group, Member

class MessageItemType(Enum):
    FriendMessage = "FriendMessage"
    GroupMessage = "GroupMessage"

class FriendMessage:
    __express_fields__ = ["messageChain", "sender"]

    type: MessageItemType = "FriendMessage"
    message_id: int
    messageChain: MessageChain
    sender: Friend

    @classmethod
    def parser(cls, value: dict):
        self = cls()
        self.messageChain = MessageChain([
            UsableMessages[i['type']].parser(i) for i in value['messageChain']
        ])
        self.sender = Friend.parser(value['sender'])

        self.message_id = self.messageChain.messages[0].uid
        return self

    def __repr__(self):
        return f"""<{self.__class__.__name__} { 
            " ".join([f"{name}={value}" for name, value in (
                {i: getattr(self, i) for i in self.__express_fields__}
            ).items()])
        }>"""

class GroupMessage:
    __express_fields__ = ["messageChain", "sender"]

    type: MessageItemType = "GroupMessage"
    messageChain: MessageChain
    sender: Member

    @classmethod
    def parser(cls, value: dict):
        self = cls()
        self.messageChain = MessageChain([
            UsableMessages[i['type']].parser(i) for i in value['messageChain']
        ])
        self.sender = Member.parser(value['sender'])
        return self

    def __repr__(self):
        return f"""<{self.__class__.__name__} { 
            " ".join([f"{name}={value}" for name, value in (
                {i: getattr(self, i) for i in self.__express_fields__}
            ).items()])
        }>"""

ItemTypes = {
    "GroupMessage": GroupMessage,
    "FriendMessage": FriendMessage
}