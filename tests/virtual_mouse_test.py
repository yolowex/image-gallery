import pygame as pg
import pygame.locals as pgl
from pygame import Vector2

from pygame._sdl2 import Renderer, Texture, Window  # noqa

window = None


def is_virtual():
    if window is not None:
        return window.grab and not pg.mouse.get_visible()
    else:
        return pg.event.get_grab() and not pg.mouse.get_visible()


def enable_virtual_mouse():
    if window is not None:
        window.grab = True
    else:
        pg.event.set_grab(True)

    pg.mouse.set_visible(False)
    print("Enabled virtual mouse", pg.event.get_grab(), pg.mouse.get_visible())


def disable_virtual_mouse():
    pg.event.set_grab(False)
    pg.mouse.set_visible(True)
    print("Disabled virtual mouse", pg.event.get_grab(), pg.mouse.get_visible())


def start_program():
    run = 1
    vm = Vector2(0, 0)

    while run:
        for i in pg.event.get():
            if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
                run = 0

            if i.type == pgl.KEYDOWN:
                if i.key == pgl.K_1:
                    enable_virtual_mouse()
                if i.key == pgl.K_2:
                    disable_virtual_mouse()

                if i.key == pgl.K_3:
                    print(pg.mouse.get_pos())
                    pg.mouse.set_pos(150, 150)
                    print(pg.mouse.get_pos())

        if is_virtual():
            vm += pg.mouse.get_rel()
            print(vm)


pg.init()
screen = pg.display.set_mode([800, 640])
start_program()

pg.quit()
pg.init()

window = Window(title="SDL window", size=[700, 700], resizable=False)

window.position = pg._sdl2.video.WINDOWPOS_CENTERED  # noqa
renderer = Renderer(window)

start_program()
