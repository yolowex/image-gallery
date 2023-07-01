import datetime
from pygame import Vector2

from core.common.enums import AspectRatioGroup


# this function is supposed to be used for log files, this is probably a bad name.
# todo: find a better name for this function
def log_time() :
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")
    return time_string


def lerp(a: float, b: float, t: float) -> float :
    return (1 - t) * a + b * t


def inv_lerp(a: float, b: float, v: float) -> float :
    return (v - a) / (b - a)


def remap(i_min, i_max, o_min, o_max, v) :
    t = inv_lerp(i_min, i_max, v)
    return lerp(o_min, o_max, t)


def get_aspect_ratio(size: Vector2) :
    w, h = size
    # unsafe: this code fails if h equals 0
    a = w / h

    ar = Vector2(a, 1)
    if ar.x > ar.y :
        ar.y = ar.y / ar.x
        ar.x = 1

    return ar

def get_aspect_ratio_group(aspect_ratio: Vector2):
    ar = aspect_ratio

    if ar.x < ar.y:
        return AspectRatioGroup.PORTRAIT

    if ar.x > ar.y:
        return AspectRatioGroup.LANDSCAPE

    return AspectRatioGroup.RECTANGULAR



"""
this block is here to test various helper functions 
"""
if __name__ == "__main__" :
    print(*[get_aspect_ratio(Vector2(1, 10)), get_aspect_ratio(Vector2(5, 7)), get_aspect_ratio(Vector2(30, 3)),
        get_aspect_ratio(Vector2(5, 5))])
