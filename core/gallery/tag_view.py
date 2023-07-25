from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.text_view import TextView
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class TagView:
    def __init__(self, box: RelRect):
        self.box = box
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

        self.people_box = RelRect(fun, 0.01, 0.01, 0.8, 0.05, use_param=True)
        self.people_text = TextView(self.people_box, is_entry=False, text="Add People")

    def check_events(self):
        self.people_text.check_events()

    def render(self):
        cr.renderer.draw_rect(self.box.get())
        self.people_text.render()
