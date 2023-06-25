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
    _id = 0
    def __init__(self,path:str):
        self.path = path
        self.level: LogLevel = LogLevel.DEBUG

        json.dump({}, open(self.path, 'w'),indent=4)


    # replace with a better name
    def write_log( self,message,log_level: LogLevel ):
        # todo: optimize file operations
        if log_level.value >= self.level.value:
            time_ = log_time()
            key = "id:"+str(Log._id)+" time:"+time_+" level:"+log_level.name
            print(key+" : "+message)

            file = open(self.path,'r')
            readfile = file.read()
            dict_ = json.loads(readfile)
            dict_[key] = message
            json.dump(dict_,open(self.path,'w'),indent=4)
            Log._id += 1





