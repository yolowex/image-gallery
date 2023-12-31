from core.common import assets
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from core.gallery.detailed_view import DetailedView
from core.gallery.fullscreen_view import FullscreenView
from gui.context_menu import ContextMenu
from gui.hover_man import HoverMan


class Gallery:
    def __init__(self):
        self.content_manager = ContentManager("")
        self.hover_man = HoverMan()
        self.context_menu = ContextMenu()
        self.content_manager.init_contents()

        self.detailed_view: DetailedView = DetailedView(
            self.content_manager, self.hover_man, self.context_menu
        )
        self.fullscreen_view: FullscreenView = FullscreenView(
            self.content_manager, self.hover_man
        )
        self.__current_view: ViewType = ViewType.DETAILED

    def init(self):
        self.detailed_view.init()
        self.fullscreen_view.init()

    def get_current_view(self):
        return self.__current_view

    def update_current_view(self, to: ViewType):
        self.__current_view = to

        if to == ViewType.FULLSCREEN:
            self.detailed_view.zoom_view.sync(self.fullscreen_view.zoom_view)
            cr.window.set_fullscreen(True)

        elif to == ViewType.DETAILED:
            self.fullscreen_view.zoom_view.sync(self.detailed_view.zoom_view)
            self.detailed_view.resize_boxes()
            cr.window.set_windowed()

    def check_events(self):
        # cr.log.was_updated = False
        if not self.context_menu.is_open and not cr.clipboard.has_popup:
            self.hover_man.update_text(None)
            self.content_manager.check_events()
            if self.__current_view == ViewType.DETAILED:
                self.detailed_view.check_events()
            elif self.__current_view == ViewType.FULLSCREEN:
                self.fullscreen_view.check_events()

            self.hover_man.check_events()

        self.context_menu.check_events()

        self.content_manager.was_updated = False

        cr.clipboard.check_events()

    def render_debug(self):
        if self.__current_view == ViewType.DETAILED:
            self.detailed_view.render_debug()

        elif self.__current_view == ViewType.FULLSCREEN:
            self.fullscreen_view.render_debug()

    def render(self):
        if self.__current_view == ViewType.DETAILED:
            self.detailed_view.render()
        elif self.__current_view == ViewType.FULLSCREEN:
            self.fullscreen_view.render()

        if not self.context_menu.is_open:
            self.hover_man.render()

        self.context_menu.render()

        if cr.event_holder.should_render_debug:
            self.render_debug()
