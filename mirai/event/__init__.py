from collections import namedtuple
from typing import Any
from enum import Enum
from pydantic import BaseModel

# 内部事件实现.
InternalEvent = namedtuple("Event", ("name", "body"))

from .enums import ExternalEventTypes
class ExternalEvent(BaseModel):
    type: ExternalEventTypes