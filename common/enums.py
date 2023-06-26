from enum import Enum

class TaskEnum(Enum):
    Fail            = 'fail'
    Success         = 'success'
    Pending         = 'pending'

class LogLevel(Enum):
    DEBUG           = 0
    INFO            = 1
    WARNING         = 2
    ERROR           = 3
    CRITICAL        = 4