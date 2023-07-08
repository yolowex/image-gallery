from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class ThumbnailView:
    def __init__(self, box: RelRect, content_manager: ContentManager):
        self.box = box
        self.content_manager = content_manager

        self.boxes: list[RelRect] = []
        self.scroll_value = 0
        self.size = len(self.content_manager.content_list)
        self.scroll_locked = False

        self.update(first_call=True)
        self.dont_reset_cursor = False

    @property
    def __scroll_bar_rect(self):
        pa = self.box.get()
        h = self.__scroll_bar_height
        x = pa.x
        y = pa.bottom - h - 1
        w = pa.w

        return FRect(x, y, w, h)

    @property
    def __scroll_button_rect(self):
        pa = self.box.get()
        bar_rect = self.__scroll_bar_rect

        val = (self.size - (pa.w // pa.h) + 1)
        if not val: val=1
        w = bar_rect.w / val

        rect = FRect(bar_rect.x + w * abs(self.scroll_value), bar_rect.y, w, bar_rect.h)

        return rect

    @property
    def __scroll_bar_height(self):
        pa = self.box.get()

        val = cr.ws().y * 0.01
        if val > pa.h * 0.1:
            val = pa.h * 0.1

        return val

    def __src_fun(self, rect):
        res = rect.copy()
        pa = self.box.get()

        h = pa.h - self.__scroll_bar_height

        res.x = (pa.x + (res.x + self.scroll_value) * h) + 1
        res.y = (pa.y + res.y * h) + 1
        res.w = res.w * h
        res.h = res.h * h
        res.w -= 2
        res.h -= 2

        return res

    def update(self, first_call=False):
        if not (self.content_manager.was_updated or first_call):
            return
        self.boxes.clear()
        for i in range(self.size):
            box = RelRect(self.__src_fun, i, 0, 1, 1, use_param=True)
            self.boxes.append(box)


    def check_scroll_bar_click(self):
        pa = self.box.get()
        mr = cr.event_holder.mouse_rect
        clicked = cr.event_holder.mouse_pressed_keys[0]

        for c, box in enumerate(self.boxes):
            this = box.get()
            if this.left < pa.left:
                continue

            if this.left > pa.right:
                continue

            content = self.content_manager.get_at(c)

            in_rect = utils.shrinked_rect(
                box.get_in_rect(Vector2(content.texture.get_rect().size)), 0.1
            )

            if mr.colliderect(in_rect) and clicked:
                self.content_manager.goto(c)
                self.dont_reset_cursor = True



    def check_scroll(self):
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = Vector2(mr.center)
        scroll_bar = self.__scroll_bar_rect
        pa = self.box.get()
        right_bound = -self.size + (pa.w // pa.h)
        clicked = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]
        should_update = False
        if (
            mr.colliderect(pa)
            or cr.event_holder.window_resized
            or cr.gallery.detailed_view.just_resized_boxes
        ):
            if (
                mw != 0
                or cr.event_holder.window_resized
                or cr.gallery.detailed_view.just_resized_boxes
            ):
                self.scroll_value += mw * 1

                should_update = True

        if mr.colliderect(scroll_bar) and clicked:
            self.scroll_locked = True

        if released:
            self.scroll_locked = False

        if self.scroll_locked:
            point_lerp = utils.inv_lerp(pa.x, pa.x + pa.w, mp.x)
            self.scroll_value = int(utils.lerp(0, right_bound, point_lerp))

            should_update = True

        if self.content_manager.was_updated and not self.dont_reset_cursor:
            self.scroll_value = -self.content_manager.current_content_index

            if self.scroll_value > 0:
                self.scroll_value = 0
            if self.scroll_value < right_bound:
                self.scroll_value = right_bound

        if should_update:
            if self.scroll_value > 0:
                self.scroll_value = 0
            if self.scroll_value < right_bound:
                self.scroll_value = right_bound

            self.content_manager.load_contents(-int(self.scroll_value))

    def check_events(self):
        self.dont_reset_cursor = False
        self.update()
        self.check_scroll_bar_click()
        self.check_scroll()

    def render_debug(self):
        ...

    def render(self):
        pa = self.box.get()
        cr.renderer.draw_color = constants.colors.GIMP_1
        cr.renderer.fill_rect(self.__scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.BEIGE
        cr.renderer.draw_rect(self.__scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.NEON
        cr.renderer.fill_rect(self.__scroll_button_rect)

        for c, box in enumerate(self.boxes):
            this = box.get()
            if this.left < pa.left:
                continue

            if this.left > pa.right:
                continue

            if c == self.content_manager.current_content_index:
                box.render(
                    constants.colors.GIMP_2,
                    constants.colors.GIMP_0,
                    constants.colors.NEON,
                )

            content = self.content_manager.get_at(c)

            in_rect = utils.shrinked_rect(
                box.get_in_rect(Vector2(content.texture.get_rect().size)), 0.1
            )
            content.render(in_rect)

        if cr.event_holder.should_render_debug:
            self.render_debug()
