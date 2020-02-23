from enum import Enum
import typing as T
from uuid import UUID
from mirai.misc import findKey, printer, ImageRegex, getMatchedString, randomRangedNumberString as rd
from mirai.face import QQFaces
from mirai.message.base import BaseMessageComponent, MessageComponentTypes
from pydantic import Field, validator
from pydantic.generics import GenericModel
from mirai.network import fetch, session
from mirai.misc import ImageType
from io import BytesIO
from PIL import Image as PILImage
from pathlib import Path
import re

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
    id: int

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
    imageId: UUID

    @validator("imageId", always=True, pre=True)
    @classmethod
    def imageId_formater(cls, v):
        if isinstance(v, str):
            imageType = "group"
            uuid_string = getMatchedString(re.search(ImageRegex[imageType], v))
            if not uuid_string:
                imageType = "friend"
                uuid_string = getMatchedString(re.search(ImageRegex[imageType], v))
            if uuid_string:
                return UUID(uuid_string)
        elif isinstance(v, UUID):
            return v

    def toString(self):
        return f"[Image::{self.imageId}]"

    @property
    def url(self):
        return f"http://gchat.qpic.cn/gchatpic_new/{rd()}/{rd()}-{rd()}-{self.imageId.hex.upper()}/0"

    def asGroupImage(self) -> str:
        return f"{{{str(self.imageId).upper()}}}.jpg"

    def asFriendImage(self) -> str:
        return f"/{str(self.imageId)}"

    async def getPillowImage(self) -> PILImage.Image:
        async with session.get(self.url) as response:
            return PILImage.open(BytesIO(await response.read()))

    @classmethod
    async def fromFileSystem(cls, 
            path: T.Union[Path, str],
            miraiSession: "MiraiProtocol",
            imageType: ImageType
        ) -> "Image":
        return await miraiSession.uploadImage(imageType, path)

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
from mirai.prototypes.context import (
    MessageContextBody,
    EventContextBody
)
from mirai.protocol import MiraiProtocol