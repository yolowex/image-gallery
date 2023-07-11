from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class HoverMan:
    """
    This class shows information about anything in a text format,
    while the user is hovering the mouse on an item or picture.

    """

    def __init__(self):
        self.mouse_move_timer = utils.now()
        self.mouse_move_trigger_time = 1
        self.text: Optional[str] = "This is textual content " * 5
        self.line_char_limit = 25
        self.last_should_render = False
        self.should_render = False
        self.font = assets.fonts["small"]
        self.texture: Optional[Texture] = None
        self.font_color = colors.WHITE
        self.bg_color = colors.GIMP_2
        self.border_color = colors.GIMP_0

        # padding values are a percentage of the window's size dimensions
        self.padding_x = 0.025
        self.padding_y = 0.025
        self.top_left = Vector2(0, 0)

    @property
    def rect(self):
        size = self.texture.get_rect().size
        rect = FRect(self.top_left, size)
        return rect

    def get_text_str(self):
        limit = self.line_char_limit
        start = 0
        end = 1

        text = ""

        while True:
            if start * limit > len(self.text):
                break

            text += self.text[start * limit : end * limit] + "\n"

            start += 1
            end += 1

        return text

    def update_text(self, text):
        if not self.should_render:
            self.text = text

    def init_text(self):
        if self.text is None:
            return

        ws = cr.ws()
        self.top_left = cr.event_holder.mouse_pos.copy()

        text = self.get_text_str()
        surface = self.font.render(text, True, self.font_color)
        new_surface = Surface(
            (
                surface.get_width() + ws.x * self.padding_x,
                surface.get_height() + ws.y * self.padding_y,
            )
        )

        new_surface.fill(self.bg_color)

        rect = surface.get_rect(center=new_surface.get_rect().center)
        new_surface.blit(surface, rect)

        self.texture = Texture.from_surface(cr.renderer, new_surface)

    def update_should_render(self):
        mr = cr.event_holder.mouse_rect
        mw = cr.event_holder.mouse_wheel
        mc = cr.event_holder.mouse_pressed_keys

        if self.should_render:
            self.should_render = mr.colliderect(self.rect) and not (mw != 0 or any(mc))
            if not self.should_render:
                self.mouse_move_timer = utils.now()
        else:
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
                self.init_text()

    def render(self):
        if self.text is None:
            return

        if self.should_render:
            self.texture.draw(None, self.rect)

            cr.renderer.draw_color = self.border_color
            cr.renderer.draw_rect(self.rect)
