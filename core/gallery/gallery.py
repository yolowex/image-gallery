from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.names import *
import core.common.resources as cr
from core.gallery.detailed_view import DetailedView
from core.gallery.fullscreen_view import FullscreenView


class Gallery:
    def __init__(self):
        self.detailed_view: DetailedView = DetailedView()
        self.fullscreen_view: FullscreenView = FullscreenView()
        self.__current_view: ViewType = ViewType.DETAILED

    def update_current_view(self,to:ViewType):
        self.__current_view = to

    def check_events(self):
        if self.__current_view == ViewType.DETAILED:
            self.detailed_view.check_events()
        elif self.__current_view == ViewType.FULLSCREEN:
            self.fullscreen_view.check_events()

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

        if cr.event_holder.should_render_debug:
            self.render_debug()
