from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
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
        self.content_load_wing = 10

        # this is set to true if the current_content_index is updated (whenever goto is used)
        self.was_updated = False

    def reinit(self, path: str = None):
        self.path: Optional[str] = path

        self.loaded_content_stack.clear()

        self.content_list.clear()
        self.current_content_index: Optional[int] = None
        self.content_load_wing = 10

        self.was_updated = False
        self.init_contents()

    def init_contents(self):
        cr.log.write_log("Initializing the contents...", LogLevel.DEBUG)

        try:
            self.content_list = [
                Content(path=i)
                for i in utils.listdir(
                    self.path,
                    constants.SUPPORTED_FILE_FORMATS,
                    False,
                    file_type=FileType.FILE,
                )
            ]
        except OSError and PermissionError as e:
            cr.log.write_log(
                f"Insufficient permission to open {self.path}, error: {e}",
                LogLevel.ERROR,
            )

        self.current_content_index = 0
        self.load_contents()
        cr.log.write_log("All contents were initialized successfully!", LogLevel.DEBUG)

    def goto(self, index):
        le = len(self.content_list) - 1
        self.current_content_index = index

        if self.current_content_index > le:
            self.current_content_index = le  # some log here
        if self.current_content_index < 0:
            self.current_content_index = 0  # and some here

        cr.log.write_log(
            f"ContentManager: {self.current_content_index+1}/{len(self.content_list)}"
            f", stack size: {len(self.loaded_content_stack)}",
            LogLevel.DEBUG,
        )

        self.load_contents()

        self.was_updated = True

    def go_next(self):
        self.goto(self.current_content_index + 1)

    def go_previous(self):
        self.goto(self.current_content_index - 1)

    def go_first(self):
        self.goto(0)

    def go_last(self):
        self.goto(len(self.content_list) - 1)

    def load_contents(self, index=None):
        if index is None:
            index = self.current_content_index

        start = index - self.content_load_wing

        if start < 0:
            start = 0

        end = index + self.content_load_wing + 1
        c = 0
        for i in self.content_list[start:end]:
            self.content_stack_add(start + c)
            if not i.is_loaded:
                i.load()

            c += 1

    def content_stack_add(self, content_index: int) -> None:
        """
        Adds a new element to the content stack, in case the stack is filled,
        the overflowed contents are unloaded from the RAM.

        :return: None
        """
        if content_index not in self.loaded_content_stack:
            self.loaded_content_stack.append(content_index)
            if len(self.loaded_content_stack) > self.loaded_content_stack_max_size:
                index = 0
                if index == self.current_content_index:
                    index = 1

                self.content_list[self.loaded_content_stack[index]].unload()
                self.loaded_content_stack.pop(index)

    @property
    def current_content(self) -> Content:
        if self.current_content_index is not None:
            if not len(self.content_list):
                return assets.app_content

            target = self.content_list[self.current_content_index]
            if target.is_loaded:
                return target
            else:
                return assets.content_placeholder

        return assets.content_placeholder

    def get_at(self, index: int) -> Content:
        try:
            if not self.content_list[index].is_loaded:
                return assets.content_placeholder

            return self.content_list[index]
        except Exception as e:
            return assets.content_placeholder

    def check_events(self):
        ...
