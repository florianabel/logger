from threading import Lock
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

    def setLogLevel(self, log_level):
        self.log_level = _checkLogLevel(log_level)

    def debug(self, msg):
        print(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def getLogger():
    return Logger()
