from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets



class ThumbnailView:
    def __init__(self, box: RelRect,content_manager:ContentManager):
        self.box = box
        self.content_manager = content_manager

        self.boxes: list[RelRect] = []
        self.scroll_value = 0
        self.size = len(self.content_manager.content_list)

        self.update(first_call=True)



    @property
    def __scroll_bar_rect(self):
        pa = self.box.get()
        h = self.__scroll_bar_height
        x = pa.x
        y = pa.bottom - h - 1
        w = pa.w

        return FRect(x,y,w,h)


    @property
    def __scroll_button_rect(self) :
        pa = self.box.get()
        bar_rect = self.__scroll_bar_rect

        w = bar_rect.w / (self.size - (pa.w // pa.h) + 1)

        rect = FRect(
            bar_rect.x + w * abs(self.scroll_value),
            bar_rect.y,
            w,
            bar_rect.h
        )

        return rect



    @property
    def __scroll_bar_height(self):
        pa = self.box.get()

        val = cr.ws().y * 0.01
        if val > pa.h * 0.1 :
            val = pa.h * 0.1

        return val

    def __src_fun(self,rect) :
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


    def update(self,first_call=False):
        if not (self.content_manager.was_updated or first_call):
            return

        for i in range(self.size):
            box = RelRect(self.__src_fun,i,0,1,1,use_param=True)
            self.boxes.append(box)


    def check_scroll(self):
        mw = cr.event_holder.mouse_wheel

        if mw != 0 or cr.event_holder.window_resized or cr.gallery.detailed_view.just_resized_boxes:

            self.scroll_value += mw * 1
            if self.scroll_value > 0:
                self.scroll_value = 0

            pa = self.box.get()
            right_bound = -self.size + (pa.w // pa.h)

            if self.scroll_value < right_bound:
                self.scroll_value = right_bound



    def check_events(self):
        self.update()
        self.check_scroll()

    def render_debug(self):
        ...

    def render(self):

        cr.renderer.draw_color = constants.Colors.GIMP_1
        cr.renderer.fill_rect(self.__scroll_bar_rect)

        cr.renderer.draw_color = constants.Colors.BEIGE
        cr.renderer.draw_rect(self.__scroll_bar_rect)

        cr.renderer.draw_color = constants.Colors.GIMP_2
        cr.renderer.fill_rect(self.__scroll_button_rect)


        for box in self.boxes:
            box.render(constants.Colors.STEEL_BLUE,constants.Colors.BLACK,constants.Colors.PLUM)

        if cr.event_holder.should_render_debug:
            self.render_debug()
