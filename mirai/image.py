import typing as T
from uuid import UUID
from enum import Enum

class ImageFormats(Enum):
    png = "png"
    jpg = "jpg"
    gif = "GIF"

class Image:
    id: UUID
    format: T.Union[ImageFormats, str]

    def __init__(self, id: UUID, format: T.Union[ImageFormats, str]):
        self.id = id
        self.format = format

    def asGroup(self):
        return f"{{{str(self.id).upper()}}}.{self.format if isinstance(self.format, str) else self.format.value}"