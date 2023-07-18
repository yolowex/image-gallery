from core.common.themes import ColorThemes
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.hover_man import HoverMan
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class TopView:
    def __init__(self, box: RelRect, hover_man: HoverMan):
        self.box = box
        self.hover_man = hover_man
        self.font: Font = assets.fonts["mid"]

        def fun(rect):
            # win_size = cr.ws()
            res = rect.copy()
            pa = self.box.get()

            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h

            res.x += pa.x
            res.y += pa.y

            return res

        self.fun = fun

        def make_fun(size):
            ar = utils.get_aspect_ratio(Vector2(size))

            def fun(rect):
                res = rect.copy()
                pa = self.box.get()

                res.x *= pa.w
                res.y *= pa.h
                res.w *= pa.h / ar.y
                res.h *= pa.h

                res.x += pa.x
                res.y += pa.y

                return res

            return fun

    def sync_texts(self):
        ...

    def check_click(self):
        click = cr.event_holder.mouse_pressed_keys[0]
        mr = cr.event_holder.mouse_rect

    def check_hover(self):
        mr = cr.event_holder.mouse_rect

    def check_events(self):
        self.check_click()
        self.check_hover()

    def render(self):
        pa = self.box.get()
