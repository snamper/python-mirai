from contextvars import ContextVar

message = ContextVar("mirai.context.message")
event = ContextVar("mirai.contexts.event")
