import typing as T

from pydantic import BaseModel

from . import BaseMessageComponent
from .components import At, AtAll, Face, Image, Plain, Source, Unknown

class MessageChain(BaseModel):
    __root__: T.List[T.Union[
        At, AtAll, Face, Image, Plain, Source, Unknown
    ]] = []

    def __add__(self, value):
        if isinstance(value, BaseMessageComponent):
            self.__root__.append(value)
            return self
        elif isinstance(value, self.__class__):
            self.__root__ += value.__root__
            return self
