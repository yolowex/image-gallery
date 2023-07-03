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
        inv_lerp(rect.x, rect.x + rect.w, abs_point.x),
        inv_lerp(rect.y, rect.y + rect.h, abs_point.y),
    )


def get_abs_point_in_rect(rel_point: Vector2, rect: FRect) -> Vector2:
    return Vector2(
        lerp(rect.x, rect.x + rect.w, rel_point.x),
        lerp(rect.y, rect.y + rect.h, rel_point.y),
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

    i = input("would you want to start the visual test? y/n: ")
    if i == 'y':
        print('cool')
    else:
        raise SystemExit


    import pygame as pg
    import pygame.locals as pgl
    from pygame import Vector2,FRect,Color
    from typing import Optional
    pg.init()
    screen = pg.display.set_mode([800,600])

    rect_1: Optional[FRect] = None
    rect_2: Optional[FRect] = None
    rel_point_1: Optional[Vector2] = None
    rel_point_2: Optional[Vector2] = None


    def reset():
        global rect_1,rect_2,rel_point_1,rel_point_2
        rect_1 = FRect(50,50,250,250)
        rect_2 = FRect(400,300,100,100)

        rel_point_1 = Vector2(0.2,0.2)
        rel_point_2 = Vector2(0.8,0.8)


    reset()
    abs_point_1 = get_abs_point_in_rect(rel_point_1,rect_1)
    abs_point_2 = get_abs_point_in_rect(rel_point_2,rect_2)

    run = True
    while run:
        trigger = False
        for i in pg.event.get():
            if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
                run = False

            if i.type == pgl.KEYDOWN:
                if i.key == pgl.K_SPACE:
                    trigger = True




        if trigger:
            rel = stack_pin(rect_1,rel_point_1,rect_2,rel_point_2)
            rect_2.center += rel
            abs_point_1 = get_abs_point_in_rect(rel_point_1, rect_1)
            abs_point_2 = get_abs_point_in_rect(rel_point_2, rect_2)


        STEEL_BLUE = Color([70, 130, 180])
        CHOCOLATE = Color([210, 105, 30])
        CRIMSON = Color([220, 20, 60])
        SPRING_GREEN = Color([0, 255, 127])
        FOREST_GREEN = Color([34, 139, 34])

        screen.fill("gray")

        pg.draw.rect(screen,CRIMSON,rect_1,2)
        pg.draw.rect(screen,FOREST_GREEN,rect_2,2)
        pg.draw.circle(screen,STEEL_BLUE,abs_point_1,6)
        pg.draw.circle(screen,STEEL_BLUE,abs_point_2,6)

        pg.display.update()





