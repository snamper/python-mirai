import typing as T
from pydantic import BaseModel

from .base import BaseMessageComponent
from ..misc import raiser, printer

class MessageChain(BaseModel):
    __root__: T.List[T.Any] = []

    def __add__(self, value):
        if isinstance(value, BaseMessageComponent):
            self.__root__.append(value)
            return self
        elif isinstance(value, MessageChain):
            self.__root__ += value.__root__
            return self

    def toString(self):
        return "".join([i.toString() for i in self.__root__])

    @classmethod
    def custom_parse(cls, value: T.List[T.Any]):
        from .components import ComponentTypes
        return cls(__root__=[
            [   
                lambda m: ComponentTypes.__members__[m['type']].value(**m),
                lambda m: raiser(TypeError("invaild value"))
            ][not isinstance(message, dict)](message) for message in value
        ])

    def __iter__(self):
        yield from self.__root__

    def __getitem__(self, index):
        return self.__root__[index]