from .session import Session
from . import (
    MessageChain,
    Plain,
    GroupMessage, FriendMessage
)

class Command:
    match_string: str

    pass

class CommandManager:
    session: Session
    registered_command = {}
    # prefix -> Union[main_name, aliases] -> action

    def __init__(self, 
            session: Session,
            listenEvents=(GroupMessage, FriendMessage)
        ):
        self.session = Session
        for event in listenEvents:
            session.receiver(event)(self.event_listener)
    
    def newCommand(self, prefix="/", addon_parser={}):
        pass

    def event_listener(self,
        session: Session,
        message: MessageChain,
        sender: "Sender",
        type: "Type"
    ):
        """用于监听事件, 并做出分析, 解析到相应的 Command 上."""
        message.toString()