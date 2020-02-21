import typing as T
from enum import Enum
from pydantic import BaseModel

class MessageComponentTypes(Enum):
    Source = "Source"
    Plain = "Plain"
    Face = "Face"
    At = "At"
    AtAll = "AtAll"
    Image = "Image"
    Unknown = "Unknown"

class BaseMessageComponent(BaseModel):
    type: MessageComponentTypes

    def toString(self):
        return self.__repr__()

from .chain import MessageChain
from mirai.message import components
from .types import MessageTypes
from mirai.message.components import (
    At,
    AtAll,
    Face,
    Plain,
    Image,
    Source
)

__all__ = [
    "At",
    "AtAll",
    "Face",
    "Plain",
    "Image",
    "Source",
    "MessageChain",

    "MessageComponents",
    "MessageTypes"
]

MessageComponents = {
    "At": components.At,
    "AtAll": components.AtAll,
    "Face": components.Face,
    "Plain": components.Plain,
    "Image": components.Image,
    "Source": components.Source,
    "Unknown": components.Unknown
}