from common.utils import *
from common.enums import LogLevel
from common.names import *

"""
this class is supposed to print the program logs
according to their log level. the higher the log level gets, 
the more important it becomes.

the logs are exported to the json file determined while initialization in path
parameter, and they contain the log level and timestamp of each log. 
"""
class Log:
    # todo: implement a convenient path handling system for all three platforms
    def __init__(self,path:str):
        self.path = path
        self.level: LogLevel = LogLevel.DEBUG

    # replace with a better name
    def write_log( self,message,log_level: LogLevel ):
        # todo: optimize file operations
        if log_level.value >= self.level.value:
            file = open(self.path,'r')
            readfile = file.read()
            dict_ = json.loads(readfile)
            key = log_time()
            dict_[key] = message
            json.dump(open(self.path,'w'),dict_)
            print(log_level.name +" "+str(message))





