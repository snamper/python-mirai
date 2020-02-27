from .session import Session
from . import (
    MessageChain,
    Plain
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
            listenEvents=("GroupMessage", "FriendMessage")):
        self.session = Session
        
    
    def newCommand(self, prefix="/", addon_parser={}):
        pass

    def event_listener(self, context):
        """用于监听事件, 并做出分析, 解析到相应的 Command 上.
        """
        context.message.messageChain: MessageChain
        context.message.messageChain.getFirstComponent(Plain)