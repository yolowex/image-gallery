from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class Spectrum:
    """
    A horizontal spectrum that is used to choose a value between 0 and 1
    """

    def __init__(
        self, box: RelRect, button_texture: Texture, on_release_function, y_scale=1
    ):
        self.font = assets.fonts["mid"]
        self.box = box
        self.src_y_scale = y_scale
        self.button_texture = button_texture
        self.on_release_function = on_release_function
        self.scroll_lock = False
        self.scroll_value = 0.5

        def make_fun(size):
            ar = utils.get_aspect_ratio(Vector2(size))

            def fun(rect):
                res = rect.copy()
                pa = self.box.get()

                res.x = pa.x
                res.y = pa.y
                res.h = pa.h
                res.w = pa.h / ar.y

                return res

            return fun

        def make_box_fun(text: Texture, box: RelRect):
            fun = make_fun(text.get_rect().size)

            def new_fun(rect, use_src=False):
                pa = box.get()
                res = fun(rect)
                src_rect = res.copy()
                src_rect.h *= self.src_y_scale
                src_rect.w *= self.src_y_scale

                if use_src:
                    res = src_rect
                else:
                    res.h *= self.y_scale
                    res.w *= self.y_scale

                # dirty: redundant
                res.centery = pa.centery

                res.centerx = utils.lerp(
                    pa.left + src_rect.w / 2,
                    pa.right - src_rect.w / 2,
                    self.scroll_value,
                )

                return res

            return new_fun

        self.make_box_fun = make_box_fun
        self.main_fun = self.make_box_fun(self.button_texture, self.box)

    @property
    def y_scale(self):
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        held = cr.event_holder.mouse_held_keys[0]

        if self.main_fun(self.box.rect, True).contains(mr):
            if held:
                return self.src_y_scale * 1.5
            else:
                return self.src_y_scale * 1.25

        if self.scroll_lock:
            return self.src_y_scale * 1.25

        return self.src_y_scale

    def check_scroll(self):
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        held = cr.event_holder.mouse_held_keys[0]
        released = cr.event_holder.mouse_released_keys[0]

        rect: FRect = self.main_fun(self.box.rect, True)

        if rect.contains(mr):
            if pressed:
                self.scroll_lock = True

        if released and self.scroll_lock:
            self.scroll_lock = False
            if callable(self.on_release_function):
                self.on_release_function()

        if self.scroll_lock:
            x = mr.centerx
            pa = self.box.get()
            self.scroll_value = utils.inv_lerp(
                pa.left + rect.w / 2, pa.right - rect.w / 2, x
            )

            if self.scroll_value < 0:
                self.scroll_value = 0
            if self.scroll_value > 1:
                self.scroll_value = 1

    def check_events(self):
        self.check_scroll()

    @property
    def bg_color(self):
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        held = cr.event_holder.mouse_held_keys[0]

        if self.box.get().contains(mr):
            if held:
                return cr.color_theme.color_1.lerp(cr.color_theme.navigator, 0.25)
            else:
                return cr.color_theme.color_1.lerp(cr.color_theme.navigator, 0.05)

        return cr.color_theme.color_1

    def render(self):
        color = self.bg_color
        cr.renderer.draw_color = color
        cr.renderer.fill_rect(self.box.get())
        cr.renderer.draw_color = cr.color_theme.color_2
        cr.renderer.draw_rect(self.box.get())

        self.button_texture.draw(None, self.main_fun(self.box.rect))
