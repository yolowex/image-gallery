from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect


class DetailedView:
    def __init__(self):
        self.current_image_rect = RelRect(cr.ws,0.2,0.1,0.78,0.7)

    def check_events(self):
        ...

    def render_debug(self):
        ...

    def render(self):
        cr.renderer.draw_color = colors.FOREST_GREEN
        cr.renderer.draw_rect(self.current_image_rect.get())


        if cr.event_holder.should_render_debug:
            self.render_debug()







