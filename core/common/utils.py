import datetime

# this function is supposed to be used for log files, this is probably a bad name.
# todo: find a better name for this function
def log_time():
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")
    return time_string

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + b * t


def inv_lerp(a: float, b: float, v: float) -> float:
    return (v - a) / (b - a)

def remap(i_min, i_max, o_min, o_max, v):
    t = inv_lerp(i_min, i_max, v)
    return lerp(o_min, o_max, t)
