from enum import Enum
import typing as T
from uuid import UUID
from mirai.misc import findKey
from mirai.face import faces

class MessageTypes(Enum):
    Source = "Source"
    Plain = "Plain"
    Face = "Face"
    At = "At"
    AtAll = "AtAll"
    Image = "Image"

class BaseMessage(object):
    __express_fields__ = ["type"]
    __static_fields__ = ["type"]
    __optional_fields__ = []

    type: MessageTypes

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__express_fields__:
                if key not in self.__static_fields__:
                    setattr(self, key, value)
                else:
                    raise KeyError(f"{key} is not able to change.")
            else:
                raise KeyError(f"{key} is not able to express.")

    def render(self):
        return {
            i: getattr(self, i) for i in self.__express_fields__\
                if (i not in self.__optional_fields__) or getattr(self, i)
        }

    def toString(self):
        return self.__repr__()
    
    @classmethod
    def parser(cls, value: dict):
        self = cls()
        for field_name in self.__express_fields__:
            if field_name not in value:
                if field_name not in self.__optional_fields__:
                    raise ValueError("wrong message model.")
            else:
                if field_name in self.__static_fields__:
                    if value.get(field_name) != getattr(self, field_name):
                        raise ValueError("you cannot change a static value.")
                setattr(self, field_name, value[field_name])
        return self

    def __repr__(self):
        return f"""<{self.__class__.__name__} { 
            " ".join([f"{name}='{value}'" for name, value in (
                {i: getattr(self, i) for i in self.__express_fields__}
            ).items()])
        }>"""

    def __add__(self, value: "BaseMessage"):
        return MessageChain([self, value])

class PlainMessage(BaseMessage):
    __express_fields__ = ["type", "text"]

    type = "Plain"
    text: str

    def toString(self):
        return self.text

class SourceMessage(BaseMessage):
    __express_fields__ = ["type", "uid"]

    type = "Source"
    uid: int

    def toString(self):
        return ""

class AtMessage(BaseMessage):
    __express_fields__ = ["type", "target", "display"]
    #__optional_fields__ = ['display']

    type = "At"
    target: int
    display: T.Optional[str] = ""

    def toString(self):
        return f"[At::target={self.target}]"

class AtAllMessage(BaseMessage):
    type = "AtAll"

    def toString(self):
        return "@全体成员"

class FaceMessage(BaseMessage):
    __express_fields__ = ["type", "faceId"]

    type = "Face"
    faceId: int

    def toString(self):
        return f"[{findKey(faces, self.faceId)}]"

class ImageMessage(BaseMessage):
    __express_fields__ = ["type", "imageId"]

    type = "Image"
    imageId: str

    def toString(self):
        return f"[Image::{self.imageId}]"

class UnknownMessage(BaseMessage):
    __express_fields__ = ["type", "text"]
    __static_fields__ = ["type", "text"]

    type = "Unknown"
    text: str = "未知消息类型"

    def toString(self):
        return ""

from .chain import MessageChain

__all__ = [
    "MessageTypes",
    "BaseMessage",
    "AtMessage",
    "AtAllMessage",
    "FaceMessage",
    "PlainMessage",
    "ImageMessage",
    "SourceMessage",
    "MessageChain",

    "UsableMessages"
]

UsableMessages = {
    "At": AtMessage,
    "AtAll": AtAllMessage,
    "Face": FaceMessage,
    "Plain": PlainMessage,
    "Image": ImageMessage,
    "Source": SourceMessage,
    "Unknown": UnknownMessage
}