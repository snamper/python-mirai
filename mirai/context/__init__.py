from contextvars import ContextVar

message = ContextVar("mirai.context.message")
event = ContextVar("mirai.contexts.event")

class _DirectPrototype:
    @property
    def message(self):
        return message.get()

    @property
    def event(self):
        return event.get()

Direct = _DirectPrototype()