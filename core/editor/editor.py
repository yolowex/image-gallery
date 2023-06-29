from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr

class Editor:
    def __init__(self):
        ...

    def check_events(self):
        ...

    def render_debug(self):
        ...


    def render(self) :
        cr.renderer.draw_color = Color("red")
        cr.renderer.clear()

        if cr.event_holder.should_render_debug :
            self.render_debug()








