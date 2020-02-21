from enum import Enum
import typing as T
from uuid import UUID
from mirai.misc import findKey
from mirai.face import QQFaces
from mirai.message.base import BaseMessageComponent, MessageComponentTypes
from pydantic import Field

__all__ = [
    "Plain",
    "Source",
    "At",
    "AtAll",
    "Face",
    "Image",
    "Unknown"
]

class Plain(BaseMessageComponent):
    type: MessageComponentTypes = "Plain"
    text: str

    def toString(self):
        return self.text

class Source(BaseMessageComponent):
    type: MessageComponentTypes = "Source"
    uid: int

    def toString(self):
        return ""

class At(BaseMessageComponent):
    type: MessageComponentTypes = "At"
    target: int
    display: T.Optional[str]

    def toString(self):
        return f"[At::target={self.target},group={message.get().message.sender.group.id},sender={message.get().message.sender.id}]"

class AtAll(BaseMessageComponent):
    type: MessageComponentTypes = "AtAll"

    def toString(self):
        return f"[AtAll::group={message.get().message.sender.group.id},sender={message.get().message.sender.id}]"

class Face(BaseMessageComponent):
    type: MessageComponentTypes = "Face"
    faceId: int

    def toString(self):
        return f"[{findKey(QQFaces, self.faceId)}]"

class Image(BaseMessageComponent):
    type: MessageComponentTypes = "Image"
    imageId: str

    def toString(self):
        return f"[Image::{self.imageId}]"

class Unknown(BaseMessageComponent):
    type: MessageComponentTypes = "Unknown"
    text: str

    def toString(self):
        return ""

class ComponentTypes(Enum):
    Plain = Plain
    Source = Source
    At = At
    AtAll = AtAll
    Face = Face
    Image = Image
    Unknown = Unknown

MessageComponents = {
    "At": At,
    "AtAll": AtAll,
    "Face": Face,
    "Plain": Plain,
    "Image": Image,
    "Source": Source,
    "Unknown": Unknown
}

from ..context import message, event