from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils


class Button:
    __id = 0

    def __init__(
        self, name: str, rel_rect: RelRect, image: Texture, on_click_action=None
    ):
        self.id_ = Button.__id
        Button.__id += 1
        self.name = name
        self.rel_rect: RelRect = rel_rect
        self.image = image
        self.on_click_action = on_click_action
        self.is_hovered = False

    def check_events(self):
        this = self.rel_rect.get()
        mr = cr.event_holder.mouse_rect
        held = cr.event_holder.mouse_held_keys[0]
        released = cr.event_holder.mouse_released_keys[0]
        self.is_hovered = False

        if mr.colliderect(this):
            self.is_hovered = True

            if released:
                if callable(self.on_click_action):
                    self.on_click_action()
                    cr.log.write_log(f"Clicked on button: {self.name} with id: {self.id_}"
                        ,LogLevel.DEBUG)

    def render_debug(self):
        ...

    def render(self):
        # mr = cr.event_holder.mouse_rect
        # this = self.rel_rect.get()
        #
        # if not mr.colliderect(this):
        #     return

        self.image.draw(None, self.rel_rect.get())

        if cr.event_holder.should_render_debug:
            self.render_debug()
