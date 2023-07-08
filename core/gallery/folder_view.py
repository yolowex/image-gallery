from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class FolderView:
    def __init__(self,box:RelRect,content_manager:ContentManager):
        self.box = box
        self.content_manager = content_manager

    def check_events(self):
        ...

    def render(self):
        ...
