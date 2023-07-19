from core.common import utils
import core.common.resources as cr
from core.common.names import *
from core.common.enums import ClipboardEnum, ClipboardResultEnum


class Clipboard:
    def __init__(self):
        self.current_operation: Optional[ClipboardEnum] = None
        self.current_result: Optional[ClipboardResultEnum] = None
        self.src_path: Optional[str] = None
        self.dst_path: Optional[str] = None

    def copy(self, path: str):
        self.current_operation = ClipboardEnum.COPY
        self.src_path = path
        self.dst_path = None

    def cut(self, path: str):
        self.current_operation = ClipboardEnum.CUT
        self.src_path = path
        self.dst_path = None
        print("cut", path)

    def __do_delete(self, path):
        ret = utils.delete(self.src_path)

        if ret:
            index = cr.gallery.content_manager.current_content_index
            cr.gallery.content_manager.reinit()
            index -= 1

            if index >= len(cr.gallery.content_manager.content_list):
                index = cr.gallery.content_manager.content_list - 1

            cr.gallery.content_manager.current_content_index = index
            cr.gallery.content_manager.load_contents()

            scroll_value = cr.gallery.detailed_view.thumbnail_view.scroll_value
            cr.gallery.detailed_view.thumbnail_view.reinit()
            cr.gallery.detailed_view.thumbnail_view.scroll_value = scroll_value
        else:
            print("Deletion failed")

    def delete(self, path: str):
        self.current_operation = ClipboardEnum.DELETE
        self.src_path = path
        print("cut", self.src_path)

        th = threading.Thread(target=lambda: self.__do_delete(self.src_path))
        th.start()

    def paste(self, path: str):
        self.dst_path = path
