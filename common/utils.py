import datetime

# this function is supposed to be used for log files, this is probably a bad name.
# todo: find a better name for this function
def log_time():
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")
    return time_string