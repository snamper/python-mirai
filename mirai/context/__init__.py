from contextvars import ContextVar

working_type = ContextVar("mirai.context.working_type")
message = ContextVar("mirai.context.message")
event = ContextVar("mirai.context.event")

class _DirectPrototype:
    @property
    def Message(self):
        return message.get()

    @property
    def Event(self):
        return event.get()

    @property
    def WorkingType(self):
        return working_type.get()

Direct = _DirectPrototype()