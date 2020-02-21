from enum import Enum
import typing as T
from uuid import UUID
from mirai.misc import findKey
from mirai.face import QQFaces
from . import BaseMessageComponent
from . import MessageComponentTypes
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
        return f"[At::target={self.target}]"

class AtAll(BaseMessageComponent):
    type: MessageComponentTypes = "AtAll"

    def toString(self):
        return "@全体成员"

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