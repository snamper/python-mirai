from contextvars import ContextVar

message = ContextVar("mirai.context.message")
event = ContextVar("mirai.contexts.event")

Direct = type("Direct", (), {
    "message": property(lambda self: message.get()),
    "event": property(lambda self: event.get())
})