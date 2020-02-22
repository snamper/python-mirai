from ..message.types import FriendMessage, GroupMessage
from pydantic import BaseModel
from ..event import ExternalEvents
from typing import Union
from ..session import Session

class MessageContextBody(BaseModel):
    message: Union[FriendMessage, GroupMessage]
    session: Session

    class Config:
        arbitrary_types_allowed = True

class EventContextBody(BaseModel):
    event: ExternalEvents
    session: Session

    class Config:
        arbitrary_types_allowed = True