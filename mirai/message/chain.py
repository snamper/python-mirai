import typing as T
from pydantic import BaseModel

from .base import BaseMessageComponent
from ..misc import raiser, printer
from .components import Source

class MessageChain(BaseModel):
    __root__: T.List[T.Any] = []

    def __add__(self, value):
        if isinstance(value, BaseMessageComponent):
            self.__root__.append(value)
            return self
        elif isinstance(value, MessageChain):
            self.__root__ += value.__root__
            return self

    def toString(self) -> str:
        return "".join([i.toString() for i in self.__root__])

    @classmethod
    def custom_parse(cls, value: T.List[T.Any]):
        from .components import ComponentTypes
        for i in value:
            if not isinstance(i, dict):
                raise TypeError("invaild value")
        return cls(__root__=[ComponentTypes.__members__[m['type']].value(**m) for m in value])

    def __iter__(self):
        yield from self.__root__

    def __getitem__(self, index):
        return self.__root__[index]

    def hasComponent(self, component_class) -> bool:
        for i in self:
            if type(i) == component_class:
                return True
        else:
            return False

    def getFirstComponent(self, component_class) -> T.Optional[BaseMessageComponent]:
        for i in self:
            if type(i) == component_class:
                return i

    def getAllofComponent(self, component_class) -> T.List[BaseMessageComponent]:
        return [i for i in self if type(i) == component_class]

    def getSource(self) -> Source:
        return self.getFirstComponent(Source)
