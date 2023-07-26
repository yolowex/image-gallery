from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.hover_man import HoverMan
from gui.zoom_view import ZoomView
from helper_kit.relative_pos import RelPos
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class NameTag(HoverMan):
    def __init__(self, owner):
        super().__init__()
        self.rel_top_left: Optional[RelPos] = None
        self.should_render = True
        self.is_selected = False
        self.just_selected = False
        self.owner = owner

    def check_events(self):
        self.just_selected = False
        mr = cr.event_holder.mouse_rect
        mp = cr.event_holder.mouse_pos
        clicked = cr.event_holder.mouse_pressed_keys[0]

        if clicked:
            if mr.colliderect(self.rect):
                cr.mouse.enable_virtual()
                self.is_selected = True
                self.just_selected = True

        if self.is_selected and not cr.mouse.is_virtual:
            self.is_selected = False

        # dirty
        zw: ZoomView = self.owner.zoom_view
        pa = zw.get_picture_rect()

        if self.is_selected:
            x = utils.inv_lerp(pa.left, pa.right, mp.x)
            y = utils.inv_lerp(pa.top, pa.bottom, mp.y)

            if x < 0:
                x = 0
            if x > 1:
                x = 1
            if y < 0:
                y = 0
            if y > 1:
                y = 1

            self.rel_top_left.pos.update(x, y)

    @property
    def rect(self):
        zw: ZoomView = self.owner.zoom_view
        pa = zw.get_picture_rect()

        if self.texture is None:
            return FRect(0, 0, 0, 0)

        size = self.texture.get_rect().size
        rect = FRect(self.rel_top_left.get(), size)

        if rect.right > pa.right:
            rect.right = pa.right

        if rect.bottom > pa.bottom:
            rect.bottom = pa.bottom

        return rect

    def update_text(self, text, line_char_limit=25, rel_top_left: RelPos = None):
        self.rel_top_left = rel_top_left
        self.line_char_limit = line_char_limit
        self.text = text

        self.init_text()
