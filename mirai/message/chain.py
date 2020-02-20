import typing as T
from . import (
    AtMessage,
    AtAllMessage,
    FaceMessage,
    ImageMessage,
    PlainMessage,
    SourceMessage,
    UnknownMessage,

    BaseMessage
)

class MessageChain:
    messages: T.List[T.Union[
        AtMessage,
        AtAllMessage,
        FaceMessage,
        ImageMessage,
        PlainMessage,
        SourceMessage,
        UnknownMessage
    ]]

    def __init__(self, messages):
        self.messages = messages

    def render(self):
        return [i.render() for i in self.messages]

    def getMessages(self):
        return self.messages

    def indexMessage(self, index):
        return self.messages[index]

    def toString(self):
        return " ".join([message.toString() for message in self.messages if message.type != "Source"])

    @property
    def length(self):
        return len(self.messages)

    def __repr__(self):
        return f"<MessageChain length={self.length} message={self.toString()}>"

    def __next__(self):
        yield from self.messages

    def __add__(self, value):
        if isinstance(value, BaseMessage):
            self.messages.append(value)
            return self
        elif isinstance(value, self.__class__):
            self.messages += value.messages
            return self