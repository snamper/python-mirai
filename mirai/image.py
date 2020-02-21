import typing as T
from uuid import UUID
from enum import Enum
from pydantic import BaseModel

class ImageFormats(Enum):
    png = "png"
    jpg = "jpg"
    gif = "GIF"

class Image(BaseModel):
    id: UUID
    format: T.Union[ImageFormats, str]

    def asGroup(self):
        return f"{{{str(self.id).upper()}}}.{self.format if isinstance(self.format, str) else self.format.value}"