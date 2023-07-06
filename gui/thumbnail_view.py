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

        self.update(first_call=True)


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

        res.x = (pa.x + res.x * h) + 1
        res.y = (pa.y + res.y * h) + 1
        res.w *= h
        res.h *= h
        res.w -= 2
        res.h -= 2

        return res


    def update(self,first_call=False):
        if not (self.content_manager.was_updated or first_call):
            return

        print('boo yah')

        size = len(self.content_manager.content_list)

        for i in range(size):
            box = RelRect(self.__src_fun,i,0,1,1,use_param=True)
            self.boxes.append(box)


    def check_events(self):
        self.update()


    def render_debug(self):
        ...

    def render(self):
        cr.renderer.draw_color = constants.Colors.BEIGE
        cr.renderer.draw_rect(self.box.get())

        for box in self.boxes:
            box.render(constants.Colors.STEEL_BLUE,constants.Colors.BLACK,constants.Colors.PLUM)

        if cr.event_holder.should_render_debug:
            self.render_debug()
