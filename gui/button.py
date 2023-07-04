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
        self,
        name: str,
        rel_rect: RelRect,
        image: Texture,
        on_click_action=None,
        render_condition=None,
    ):
        self.id_ = Button.__id
        Button.__id += 1
        self.name = name
        self.rel_rect: RelRect = rel_rect
        self.image = image
        self.on_click_action = on_click_action
        """
        the conditions that have to be met in order to render this buttons,
        this has to be a callable object, and return either false or true.
        """
        self.render_condition = render_condition
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
                    cr.log.write_log(
                        f"Clicked on button: {self.name} with id: {self.id_}",
                        LogLevel.DEBUG,
                    )

                    try:
                        self.on_click_action()

                    except Exception as e:
                        cr.log.write_log(
                            f"Could not call on_click_action for {self.name} button"
                            "due to this error: {e}",
                            LogLevel.ERROR,
                        )

    def render_debug(self):
        ...

    def render(self):
        if not (
            not callable(self.render_condition)
            or (callable(self.render_condition) and self.render_condition())
        ):
            return

        self.image.draw(None, self.rel_rect.get())

        if cr.event_holder.should_render_debug:
            self.render_debug()
