from core.common import assets
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from gui.image_ui_layer import ImageUiLayer
from gui.zoom_view import ZoomView
from helper_kit.relative_rect import RelRect
from core.common.constants import Colors


class FullscreenView:
    def __init__(self,content_manager:ContentManager):
        self.image_box = RelRect(cr.ws, (0, 0), (1, 1))
        self.content_manager = content_manager
        zoom_texture = random.choice(assets.pics)
        self.zoom_view = ZoomView(self.image_box, zoom_texture,self.content_manager)
        self.image_ui_layer = ImageUiLayer()

    def init(self):
        self.image_ui_layer.init()

    def check_events(self):
        self.image_ui_layer.check_events()
        self.zoom_view.update()
        if not self.image_ui_layer.any_hovered:
            self.zoom_view.check_events()

    def render_debug(self):
        ...

    def render(self):
        self.image_box.render(Colors.GIMP_1, Colors.GIMP_2, Colors.GIMP_0)
        self.zoom_view.render()
        self.image_ui_layer.render()
        if cr.event_holder.should_render_debug:
            self.render_debug()
