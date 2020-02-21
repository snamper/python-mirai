from enum import Enum
from pydantic import BaseModel

__all__ = [
    "MessageComponentTypes",
    "BaseMessageComponent"
]

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