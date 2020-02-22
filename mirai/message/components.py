from enum import Enum
import typing as T
from uuid import UUID
from mirai.misc import findKey, printer, justdo
from mirai.face import QQFaces
from mirai.message.base import BaseMessageComponent, MessageComponentTypes
from pydantic import Field, validator
from pydantic.generics import GenericModel

__all__ = [
    "Plain",
    "Source",
    "At",
    "AtAll",
    "Face",
    "Image",
    "Unknown"
]

TempType = T.TypeVar("TempType")

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

class At(GenericModel, BaseMessageComponent):
    type: MessageComponentTypes = "At"
    target: int

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
        return f"[Face::key={findKey(QQFaces, self.faceId)}]"

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