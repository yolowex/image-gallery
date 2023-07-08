from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from helper_kit.relative_rect import RelRect
from core.common import utils, assets

class InfoView:
    def __init__(self,box:RelRect):
        self.box = box
        self.font = assets.fonts['mid']


    def check_events(self):
        ...

    def render(self):
        cr.renderer.draw_color = colors.INDIGO
        cr.renderer.fill_rect(self.box.get())












# todo: find a better name for this class
