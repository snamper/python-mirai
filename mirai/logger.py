import logging

logging.basicConfig(
    format="[time::%(asctime)s][thread::%(thread)d]<%(levelname)s>: %(message)s",
    level=20
)

network = logging.getLogger("network")
event = logging.getLogger("event")
message = logging.getLogger("message")
normal = logging.getLogger("normal")

normal.debug("logger init finished.")