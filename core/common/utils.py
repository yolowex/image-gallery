import datetime
from pygame import Vector2, FRect

from core.common.enums import AspectRatioGroup


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


def get_aspect_ratio(size: Vector2):
    w, h = size
    # unsafe: this code fails if h equals 0
    a = w / h

    ar = Vector2(a, 1)
    if ar.x > ar.y:
        ar.y = ar.y / ar.x
        ar.x = 1

    if ar.x < 1:
        ar.y = ar.y * (1 / ar.x)
        ar.x = 1
        # print("ar",size,ar)

    return ar


def get_aspect_ratio_group(aspect_ratio: Vector2):
    ar = aspect_ratio

    if ar.x < ar.y:
        return AspectRatioGroup.PORTRAIT

    if ar.x > ar.y:
        return AspectRatioGroup.LANDSCAPE

    return AspectRatioGroup.RECTANGULAR


def get_rel_point_in_rect(abs_point: Vector2, rect: FRect) -> Vector2:
    return Vector2(
        inv_lerp(0, rect.w, abs_point.x),
        inv_lerp(0, rect.h, abs_point.y),
    )


def get_abs_point_in_rect(rel_point: Vector2, rect: FRect) -> Vector2:
    return Vector2(
        lerp(rect.x, rect.w, rel_point.x),
        lerp(rect.y, rect.h, rel_point.y),
    )


# todo: add doc string for this function
def stack_pin(
    rect_1: FRect, rel_point_1: Vector2, rect_2: FRect, rel_point_2: Vector2
) -> Vector2:
    """

    :return:
    """

    abs_point_1 = get_abs_point_in_rect(rel_point_1, rect_1)
    abs_point_2 = get_abs_point_in_rect(rel_point_2, rect_2)

    return abs_point_1  -abs_point_2


"""
this block is here to test various helper functions 
"""
if __name__ == "__main__":
    for i in range(1, 3):
        for c in range(1, 3):
            ar = get_aspect_ratio(Vector2(i, c))
            arg = get_aspect_ratio_group(ar)
            print((i, c), ar, arg)

    rect = FRect(0, 0, 150, 150)
    rect2 = FRect(50, 50, 300, 300)

    rel_point = get_rel_point_in_rect(Vector2(30, 30), rect)
    abs_point = get_abs_point_in_rect(rel_point, rect2)

    print(stack_pin(rect, Vector2(0.5, 0.5), rect2, Vector2(0.5, 0.5)))
