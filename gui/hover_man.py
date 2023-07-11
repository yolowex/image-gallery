from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils


class HoverMan:
    """
    This class shows information about anything in a text format,
    while the user is hovering the mouse on an item or picture.

    """

    def __init__(self):
        self.mouse_move_timer = utils.now()
        self.mouse_move_trigger_time = 1
        self.text: Optional[str] = "This is textual content"
        self.last_should_render = False
        self.should_render = False

    def init_text(self, text: str = None):
        ...

    def update_should_render(self):
        self.should_render = (
            utils.now() > self.mouse_move_timer + self.mouse_move_trigger_time
        )

    def check_events(self):
        self.last_should_render = self.should_render
        self.update_should_render()

        if cr.event_holder.mouse_moved:
            self.mouse_move_timer = utils.now()

        if self.should_render:
            if not self.last_should_render:
                print("Trigger")

    def render(self):
        ...
