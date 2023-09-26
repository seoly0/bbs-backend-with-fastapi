import logging

from asgi_correlation_id import CorrelationIdFilter

from .base import BootBase

FORMAT = "[\033[%(levelcolor)s%(levelname)-8s\033[0m] :: %(asctime)s ::%(ridformat)s %(name)s >> %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

color = {
    logging.DEBUG: "33m",
    logging.INFO: "96m",
    logging.WARN: "38;5;208m",
    logging.WARNING: "38;5;208m",
    logging.ERROR: "31m",
    logging.CRITICAL: "31m",
}


class MyFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        record.levelcolor = color.get(record.levelno)
        record.ridformat = f" {record.correlation_id} ::" if record.correlation_id else ""
        return logging.Formatter(FORMAT).format(record)


class LoggerBoot(BootBase):
    def execute(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.addFilter(CorrelationIdFilter())
        handler.setFormatter(MyFormatter())

        logging.basicConfig(datefmt=DATE_FORMAT, level=logging.DEBUG, handlers=[handler])


boot = LoggerBoot()
order = 1
