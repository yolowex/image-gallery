import threading

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
        self.loaded_content_stack_max_size = 50
        self.content_list: list[Content] = []
        self.current_content_index: Optional[int] = None
        self.content_load_wing = 10

        # this is set to true if the current_content_index is updated (whenever goto is used)
        self.was_updated = False
        self.audio_thread_occupied = False
        self.current_audio_thread: Optional[Content] = None
        self.audio_thread_queue: Optional[Content] = None

    def reinit(self, path: str = None):
        if path is None:
            path = self.path

        cr.gallery.detailed_view.tag_view.load()

        self.destroy_audio()

        self.path: Optional[str] = path

        self.loaded_content_stack.clear()

        self.content_list.clear()
        self.current_content_index: Optional[int] = None
        self.content_load_wing = 10

        self.was_updated = False
        self.init_contents()
        cr.gallery.detailed_view.top_view.sync_texts()
        cr.gallery.detailed_view.tag_view.load()

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

            self.content_list.sort(key=lambda x: x.name)

        except OSError or PermissionError or FileNotFoundError as e:
            cr.log.write_log(
                f"Insufficient permission to open {self.path}, error: {e}",
                LogLevel.ERROR,
            )

        self.current_content_index = 0
        self.load_contents()
        cr.log.write_log("All contents were initialized successfully!", LogLevel.DEBUG)

    def trigger_media(self):
        content = self.current_content

        if content.type == ContentType.VIDEO:
            if not content.video_audio_loaded:
                content.is_loading_audio = True
                if self.audio_thread_occupied:
                    self.audio_thread_queue = content
                else:
                    self.audio_thread_occupied = True
                    self.current_audio_thread = content
                    thread = threading.Thread(target=content.load_audio)
                    thread.start()
                content.start()

            else:
                if not content.video_is_started:
                    content.start()

                elif content.video_is_paused:
                    content.unpause()
                else:
                    content.pause()

    def destroy_audio(self):
        content = self.current_content

        if content.type == ContentType.VIDEO:
            content.destroy_audio()
            ui_layer = cr.gallery.detailed_view.image_ui_layer
            if cr.gallery.get_current_view() == ViewType.FULLSCREEN:
                ui_layer = cr.gallery.fullscreen_view.image_ui_layer

            ui_layer.reset_trigger_button()

    def goto(self, index):
        if self.current_content_index == index:
            return

        self.destroy_audio()

        le = len(self.content_list) - 1
        self.current_content_index = index

        if self.current_content_index > le:
            self.current_content_index = le  # some log here
        if self.current_content_index < 0:
            self.current_content_index = 0  # and some here

        # con = self.content_list[self.current_content_index]
        # print(con.ctime,con.size)

        cr.log.write_log(
            f"ContentManager: {self.current_content_index+1}/{len(self.content_list)}"
            f", stack size: {len(self.loaded_content_stack)}",
            LogLevel.DEBUG,
        )

        self.load_contents()
        cr.gallery.detailed_view.top_view.sync_texts()
        cr.gallery.detailed_view.tag_view.load()

        self.was_updated = True

    def go_next(self):
        self.goto(self.current_content_index + 1)

    def go_previous(self):
        self.goto(self.current_content_index - 1)

    def go_first(self):
        self.goto(0)

    def go_last(self):
        self.goto(len(self.content_list) - 1)

    def go_forward(self):
        self.current_content.go_forward()

    def go_back(self):
        self.current_content.go_back()

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
            if not i.is_loaded and not i.failed_to_load:
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
        if self.audio_thread_occupied:
            cr.mouse.set_high_priority(pgl.SYSTEM_CURSOR_WAIT)

            result = self.current_audio_thread.audio_extraction_result
            if result is not None:
                cr.mouse.set_high_priority(None)
                if result:
                    ...
                else:
                    ...

                self.audio_thread_occupied = False
                content = self.current_content
                if content != self.current_audio_thread:
                    self.current_audio_thread.audio_extraction_result = None
                    self.current_audio_thread.video_audio_loaded = False

                if self.audio_thread_queue is not None:
                    self.current_audio_thread = self.audio_thread_queue
                    self.audio_thread_occupied = True
                    thread = threading.Thread(
                        target=self.current_audio_thread.load_audio
                    )
                    thread.start()
                    self.audio_thread_queue = None
