from logbook import Logger, StreamHandler
from logbook import (
    INFO,
    DEBUG
)
import sys

stream_handler = StreamHandler(sys.stdout, level=INFO)
stream_handler.format_string = '[{record.time:%Y-%m-%d %H:%M:%S}][Mirai] {record.level_name}: {record.channel}: {record.message}'
stream_handler.push_application()

Event = Logger('Event', level=INFO)
Network = Logger("Network", level=DEBUG)
Session = Logger("Session", level=INFO)
Protocol = Logger("Protocol", level=INFO)