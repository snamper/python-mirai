from ..message.types import FriendMessage, GroupMessage
from pydantic import validator, BaseModel
from ..event import ExternalEvents
from typing import Union
from contextvars import ContextVar
from ..session import Session
from ..protocol import MiraiProtocol
import asyncio

message = ContextVar("mirai.context.message")
event = ContextVar("mirai.contexts.event")
