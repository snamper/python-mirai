from .message.types import FriendMessage, GroupMessage
from pydantic import validator, BaseModel
from .event import ExternalEvents
from typing import Union
from contextvars import ContextVar
from .session import Session
from .protocol import MiraiProtocol
import asyncio

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



message: ContextVar[MessageContextBody] = ContextVar("mirai.context.message")
event: ContextVar[EventContextBody] = ContextVar("mirai.contexts.event")
