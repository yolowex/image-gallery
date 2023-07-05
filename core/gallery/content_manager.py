from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class ContentManager:
    """
    this class manages loading and unloading the contents of a directory or a search
    result.

    """

    def __init__(self, path: str = None):
        self.path: Optional[str] = path
        # stores the index number of loaded contents which reside in the content_list
        self.loaded_content_stack: list[int] = []
        self.loaded_content_stack_max_size = 100
        self.content_list: list[Content] = []
        self.current_content_index: Optional[int] = None

        self.content_load_wing = 5

    def init_contents(self):
        cr.log.write_log("Initializing the contents...",LogLevel.DEBUG)
        self.content_list = [Content(path=i) for i in
            utils.listdir(
            self.path, constants.SUPPORTED_FILE_FORMATS, False
        )]


        self.current_content_index = 0
        self.load_contents()
        cr.log.write_log("All contents were initialized successfully!",LogLevel.DEBUG)


    def load_contents(self):
        start = self.current_content_index - self.content_load_wing

        if start < 0:
            start = 0

        end = self.current_content_index + self.content_load_wing
        for i in self.content_list[start:end]:
            i.load()

    def content_stack_add(self, content_index: int) -> None:
        """
        Adds a new element to the content stack, in case the stack is filled,
        the overflowed contents are unloaded from the RAM.

        :return: None
        """
        self.loaded_content_stack.insert(0, content_index)
        if len(self.loaded_content_stack) >= self.loaded_content_stack_max_size:
            self.content_list[self.loaded_content_stack[-1]].unload()
            self.loaded_content_stack.pop(-1)

    @property
    def current_content(self) -> Content:
        if self.current_content_index is not None:
            target = self.content_list[self.current_content_index]
            if target.is_loaded:
                return target
            else:
                return assets.content_placeholder

        return assets.content_placeholder

    def check_events(self):
        ...
