import sys
from datetime import datetime
from threading import Lock
from collections import namedtuple


# Records
Record = namedtuple("Record", "log_level msg")


# Log level
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40

_name_to_log_level = {
    'DEBUG': DEBUG,
    'INFO': INFO,
    'WARNING': WARNING,
    'ERROR': ERROR,
}

_log_level_to_name = {
    DEBUG: 'DEBUG',
    INFO: 'INFO',
    WARNING: 'WARNING',
    ERROR: 'ERROR',
}


def _checkLogLevel(log_level):
    if isinstance(log_level, int):
        lv = log_level
    elif isinstance(log_level, str):
        if log_level not in _name_to_log_level:
            raise ValueError(f"Unknown log level: {log_level}")
        lv = _name_to_log_level[log_level]
    else:
        raise TypeError(
            f"Log level is not an integer or a valid string: {log_level}")
    return lv


class Handler:
    def __init__(self, log_level=DEBUG):
        self.setLogLevel(log_level)

    def setLogLevel(self, log_level):
        self.log_level = _checkLogLevel(log_level)

    def handle(self, record):
        if record.log_level >= self.log_level:
            prefix = self._prefix(record)
            formatted_msg = f"{prefix} {record.msg}{self.terminator}"
            formatted_msg = record.msg
            self.emit(formatted_msg)

    def emit(self, formatted_msg):
        raise NotImplementedError(
            'emit must be implemented by Handler subclasses')

    def _prefix(self, record):
        return f"[{self.HANDLER_PREFIX}][{_log_level_to_name[record.log_level]}][{datetime.now()}]"


class ConsoleHandler(Handler):

    terminator = '\n'
    HANDLER_PREFIX = 'CONSOLE'

    def __init__(self):
        super().__init__()
        self.stream = sys.stdout

    def flush(self):
        self.stream.flush()
        
    def emit(self, formatted_msg):
        self.stream.write(formatted_msg)
        self.flush()


class MailHandler(Handler):

    terminator = '\n'
    HANDLER_PREFIX = 'MAIL'

    def __init__(self):
        super().__init__()
        self.stream = sys.stdout

    def flush(self):
        self.stream.flush()

    def emit(self, formatted_msg):
        self.stream.write(formatted_msg)
        self.flush()


class FileHandler(Handler):

    terminator = '\n'
    HANDLER_PREFIX = 'FILE'

    def __init__(self):
        super().__init__()
        self.stream = sys.stdout

    def flush(self):
        self.stream.flush()

    def emit(self, formatted_msg):
        self.stream.write(formatted_msg)
        self.flush()


class ApiHandler(Handler):

    terminator = '\n'
    HANDLER_PREFIX = 'API'

    def __init__(self):
        super().__init__()
        self.stream = sys.stdout

    def flush(self):
        self.stream.flush()

    def emit(self, formatted_msg):
        self.stream.write(formatted_msg)
        self.flush()


_nameToHandler = {
    'console': ConsoleHandler,
    'mail': MailHandler,
    'file': FileHandler,
    'api': ApiHandler,
}


class LoggerMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


class Logger(metaclass=LoggerMeta):
    def __init__(self, log_level=DEBUG):
        self.setLogLevel(log_level)
        self.handlers = []

    def setLogLevel(self, log_level):
        self.log_level = _checkLogLevel(log_level)

    def isEnabledFor(self, log_level):
        isEnabled = log_level >= self.log_level
        return isEnabled

    def basicConfig(self):
        self.addConsoleHandler()

    def addConsoleHandler(self):
        handler = ConsoleHandler()
        self.addHandler(handler)

    def addHandler(self, handler):
        if isinstance(handler, Handler):
            if not handler in self.handlers:
                self.handlers.append(handler)

    def debug(self, msg):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg)

    def info(self, msg):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg)

    def warning(self, msg):
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg)

    def error(self, msg):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg)

    def _log(self, level, msg):
        if len(self.handlers) == 0:
            self.basicConfig()
        record = Record(level, msg)
        self._handle(record)

    def _handle(self, record):
        for handler in self.handlers:
            if record.log_level >= handler.log_level:
                handler.handle(record)


def getLogger():
    return Logger()
