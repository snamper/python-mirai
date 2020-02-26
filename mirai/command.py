from .session import Session

class Command:
    prefix: str
    match_string: str

    pass

class CommandManager:
    session: Session

    def __init__(self, session):
        self.session = Session
    
    def newCommand(self, prefix="/", addon_parser={}):
        pass