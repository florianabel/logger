from threading import Lock
# Log level
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40


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
        self.log_level = log_level

    def setLogLevel(self, log_level):
        self.log_level = log_level


def getLogger():
    return Logger()
