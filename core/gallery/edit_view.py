from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.name_tag import NameTag
from gui.text_view import TextView
from gui.zoom_view import ZoomView
from helper_kit.relative_pos import RelPos
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class EditView:
    def __init__(self, box: RelRect):
        self.box = box
        self.font: Font = assets.fonts["mid"]

    def check_events(self):
        ...

    def render(self):
        cr.renderer.draw_rect(self.box.get())
