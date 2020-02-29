from logbook import Logger, StreamHandler
from logbook import (
    INFO,
    DEBUG
)
import sys

StreamHandler(sys.stdout, level=INFO).push_application()

Event = Logger('Event', level=INFO)
Network = Logger("Network", level=DEBUG)
Session = Logger("Session", level=INFO)
