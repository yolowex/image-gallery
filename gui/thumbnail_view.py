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


    def __src_fun(self,rect) :
        res = rect.copy()
        pa = self.box.get()

        res.x = (pa.x + res.x * pa.h) + 1
        res.y = (pa.y + res.y * pa.h) + 1
        res.w *= pa.h
        res.h *= pa.h
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
            box.render(constants.Colors.STEEL_BLUE,constants.Colors.GIMP_0,constants.Colors.PLUM)

        if cr.event_holder.should_render_debug:
            self.render_debug()
