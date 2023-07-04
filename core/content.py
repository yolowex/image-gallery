from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils

class Content:
    def __init__(self,path:str=None):
        self.path: Optional[str] = path

    def load(self):
        ...

    def check_events(self):
        ...

    def render_debug(self):
        ...

    def render(self):

        if cr.event_holder.should_render_debug:
            self.render_debug()