from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.hover_man import HoverMan
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
        hover_man_action=False,
    ):
        self.id_ = Button.__id
        Button.__id += 1
        self.name = name
        self.rel_rect: RelRect = rel_rect
        self.image = image
        self.on_click_action = on_click_action
        self.hover_man_action = hover_man_action
        """
        the conditions that have to be met in order to render this buttons,
        this has to be a callable object, and return either false or true.
        """
        self.render_condition = render_condition
        self.is_hovered = False

    def hover_man_check(self):
        hover_man: HoverMan = cr.gallery.hover_man
        mr = cr.event_holder.mouse_rect
        if mr.colliderect(self.rel_rect.get()):
            hover_man.update_text(self.name)

    def check_events(self):
        if not (
            not callable(self.render_condition)
            or (callable(self.render_condition) and self.render_condition())
        ):
            return

        self.hover_man_check()

        this = self.rel_rect.get()
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        self.is_hovered = False
        if mr.colliderect(this):
            self.is_hovered = True

            if pressed:
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
                            f"due to this error: {e}",
                            LogLevel.ERROR,
                        )

    @property
    def render_rect(self):
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        held = cr.event_holder.mouse_held_keys[0]

        rect = self.rel_rect.get()
        lc = rect.center

        if self.rel_rect.get().contains(mr):
            if held:
                rect.w *= 1.35
                rect.h *= 1.35
            else:
                rect.w *= 1.2
                rect.h *= 1.2

        rect.center = lc
        return rect

    def render(self):
        if not (
            not callable(self.render_condition)
            or (callable(self.render_condition) and self.render_condition())
        ):
            return

        self.image.draw(None, self.render_rect)
