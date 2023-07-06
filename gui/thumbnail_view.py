from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets



class ThumbnailView:
    def __init__(self,box:RelRect):
        self.box = box

    def check_events(self):
        ...

    def render_debug(self):
        ...

    def render(self):
        cr.renderer.draw_color = constants.Colors.BEIGE
        cr.renderer.draw_rect(self.box.get())

        if cr.event_holder.should_render_debug:
            self.render_debug()