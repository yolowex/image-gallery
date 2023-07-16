from core.common import assets
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from gui.hover_man import HoverMan
from gui.image_ui_layer import ImageUiLayer
from gui.zoom_view import ZoomView
from helper_kit.relative_rect import RelRect
from core.common.constants import colors


class FullscreenView:
    def __init__(self, content_manager: ContentManager, hover_man: HoverMan):
        self.image_box = RelRect(cr.ws, (0, 0), (1, 1))
        self.content_manager = content_manager
        self.hover_man = hover_man

        self.zoom_view = ZoomView(self.image_box, self.content_manager)
        self.image_ui_layer = ImageUiLayer(self.hover_man)

    def init(self):
        self.image_ui_layer.init()

    def check_events(self):
        self.image_ui_layer.check_events()

        if pgl.K_r in cr.event_holder.pressed_keys or self.content_manager.was_updated:
            self.zoom_view.reset()

        self.zoom_view.update()

        self.zoom_view.check_events()

    def render_debug(self):
        ...

    def render(self):
        theme = cr.color_theme
        self.image_box.render(theme.color_1, theme.color_2, theme.color_0)
        self.zoom_view.render()
        self.image_ui_layer.render()
        if cr.event_holder.should_render_debug:
            self.render_debug()
