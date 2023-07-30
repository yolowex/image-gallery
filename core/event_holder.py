import pygame as pg
from pygame.locals import *
from pygame.rect import FRect
from pygame.math import Vector2

from core.common import utils


class EventHolder:
    def __init__(self):
        self.pressed_keys = []
        self.released_keys = []
        self.held_keys = []
        self.window_focus = True
        self.window_resized = False

        self.__mouse_double_click_timer = 0
        self.__mouse_double_click_duration = 0.2
        self.mouse_double_clicked = False
        self.mouse_wheel = 0
        self.mouse_moved = False
        self.mouse_pos = Vector2(0, 0)
        self.mouse_pressed_keys = [False, False, False]
        self.mouse_released_keys = [False, False, False]
        self.mouse_held_keys = [False, False, False]
        self.mouse_focus = False
        self.should_render_debug = False
        self.should_quit = False
        self.determined_fps = 60
        self.final_fps = 0
        self.focus_gain_timer = -100
        self.mouse_focus_gain_timer = -100
        self.clock = pg.time.Clock()
        self.dt = 0

        self.events: list[pg.event.Event] = []

    @property
    def delta_time(self):
        return self.dt
        # delta = 1 / (self.final_fps if self.final_fps!=0 else 60)
        # return delta

    @property
    def mouse_rect(self) -> FRect:
        radius = 2
        return FRect(
            self.mouse_pos.x - radius, self.mouse_pos.y - radius, radius * 2, radius * 2
        )

    def get_events(self):
        self.pressed_keys.clear()
        self.released_keys.clear()
        self.mouse_pressed_keys = [False, False, False]
        self.mouse_released_keys = [False, False, False]

        self.mouse_moved = False
        self.final_fps = self.clock.get_fps()
        self.dt = self.clock.tick(self.determined_fps) / 1000
        self.window_resized = False
        self.mouse_wheel = 0
        self.events.clear()
        self.events.extend(pg.event.get())
        for i in self.events:
            if i.type == WINDOWFOCUSLOST:
                self.window_focus = False
            if i.type == WINDOWFOCUSGAINED:
                self.window_focus = True
                self.focus_gain_timer = pg.time.get_ticks() / 1000

            if i.type == WINDOWRESIZED:
                self.window_resized = True

            if i.type == WINDOWENTER:
                self.mouse_focus = True
                self.mouse_focus_gain_timer = pg.time.get_ticks() / 1000

            if i.type == WINDOWLEAVE:
                self.mouse_focus = False

            if i.type == WINDOWENTER or MOUSEMOTION:
                self.mouse_pos = Vector2(pg.mouse.get_pos())

            if i.type == QUIT or i.type == KEYDOWN and i.key == K_ESCAPE:
                self.should_quit = True

            if i.type == MOUSEMOTION:
                self.mouse_moved = True

            if i.type == MOUSEWHEEL:
                self.mouse_wheel = abs(i.y) / i.y

            if i.type == KEYDOWN:
                self.pressed_keys.append(i.key)
                if i.key not in self.held_keys:
                    self.held_keys.append(i.key)

            if i.type == KEYUP:
                self.released_keys.append(i.key)
                if i.key in self.held_keys:
                    self.held_keys.remove(i.key)

            # elif i.type == VIDEORESIZE : # this might be useful later
            #     new_width, new_height = i.size

            if i.type == MOUSEBUTTONDOWN:
                self.mouse_pressed_keys = list(pg.mouse.get_pressed())
                self.mouse_held_keys = list(pg.mouse.get_pressed())

            if i.type == MOUSEBUTTONUP:
                self.mouse_released_keys = list(pg.mouse.get_pressed())

                for index, released, held in zip(
                    range(3), self.mouse_released_keys, self.mouse_held_keys
                ):
                    if held and not released:
                        self.mouse_released_keys[index] = True
                    else:
                        self.mouse_released_keys[index] = False

                self.mouse_held_keys = list(pg.mouse.get_pressed())

        self.mouse_double_clicked = False

        if self.mouse_pressed_keys[0]:
            n = utils.now()
            # print(n,self.mouse_double_click_timer+self.mouse_double_click_duration)

            if n > self.__mouse_double_click_timer + self.__mouse_double_click_duration:
                self.__mouse_double_click_timer = n

            else:
                self.mouse_double_clicked = True
