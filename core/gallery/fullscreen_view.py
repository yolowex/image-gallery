from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr

class FullscreenView:
    def __init__(self):
        ...

    def check_events(self):
        ...

    def render_debug(self):
        ...

    def render(self):

        if cr.event_holder.should_render_debug:
            self.render_debug()







