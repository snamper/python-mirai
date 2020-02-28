from logbook import Logger, StreamHandler
import sys

StreamHandler(sys.stdout).push_application()

Event = Logger('Event')
Network = Logger("Network", level="DEBUG")
