from enum import Enum

class TaskEnum(Enum):
    FAIL            = 'fail'
    SUCCESS         = 'success'
    PENDING         = 'pending'

class LogLevel(Enum):
    DEBUG           = 0
    INFO            = 1
    WARNING         = 2
    ERROR           = 3
    FATAL           = 4

class ViewType(Enum):
    FULLSCREEN = 0
    DETAILED = 1