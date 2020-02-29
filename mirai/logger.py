from logbook import Logger, StreamHandler
import sys

StreamHandler(sys.stdout, level=20).push_application()

Event = Logger('Event', level=20)
Network = Logger("Network", level=10)
