import threading

from core.common import utils
import core.common.resources as cr
from core.common.names import *
from core.common.enums import ClipboardEnum, ClipboardResultEnum, LogLevel
from helper_kit.delete_popup import delete_file_popup
from helper_kit.name_dialog_popup import name_dialog


class Clipboard:
    def __init__(self):
        self.current_operation: Optional[ClipboardEnum] = None
        self.current_result: Optional[ClipboardResultEnum] = None
        self.src_path: Optional[str] = None
        self.dst_path: Optional[str] = None
        self.trigger_operation = False
        self.has_popup = False
        self.new_folder_name: Optional[str] = None

    @property
    def log_text(self):
        path = self.src_path[-35:]
        return self.current_operation.name + " " + self.current_result.name + " " + path

    def copy(self, path: str):
        self.current_result = ClipboardResultEnum.PENDING
        self.current_operation = ClipboardEnum.COPY
        self.src_path = path
        self.dst_path = None
        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def cut(self, path: str):
        self.current_result = ClipboardResultEnum.PENDING
        self.current_operation = ClipboardEnum.CUT
        self.src_path = path
        self.dst_path = None
        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def create_new_folder(self, item):
        self.current_result = ClipboardResultEnum.PENDING
        self.current_operation = ClipboardEnum.NEW_FOLDER
        self.src_path = item["path"]
        fun = lambda: name_dialog(self)
        th = threading.Thread(target=fun)
        th.start()
        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def perform_folder_creation(self):
        path = self.src_path + "/" + self.new_folder_name
        path = pathlib.Path(path).resolve()

        try:
            self.current_result = ClipboardResultEnum.SUCCESS
            os.mkdir(path)
        except OSError as e:
            self.current_result = ClipboardResultEnum.FAILED

        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def __do_delete(self, path):
        ret = utils.delete(self.src_path)

        if ret:
            index = cr.gallery.content_manager.current_content_index
            cr.gallery.content_manager.reinit()

            if index >= len(cr.gallery.content_manager.content_list):
                index = cr.gallery.content_manager.content_list.__len__() - 1

            cr.gallery.content_manager.current_content_index = index
            cr.gallery.content_manager.load_contents()

            scroll_value = cr.gallery.detailed_view.thumbnail_view.scroll_value
            cr.gallery.detailed_view.thumbnail_view.reinit()
            cr.gallery.detailed_view.thumbnail_view.scroll_value = scroll_value
            self.current_result = ClipboardResultEnum.SUCCESS

        else:
            self.current_result = ClipboardResultEnum.FAILED

        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def __do_copy(self, src_path, dst_path, is_cut):
        ret = utils.copy(src_path, dst_path, is_cut)

        src = os.path.dirname(src_path)

        if ret:
            if cr.gallery.content_manager.path in dst_path or (
                cr.gallery.content_manager.path == src and is_cut
            ):
                index = cr.gallery.content_manager.current_content_index
                cr.gallery.content_manager.reinit()

                if is_cut:
                    index -= 1
                    if index >= len(cr.gallery.content_manager.content_list):
                        index = cr.gallery.content_manager.content_list - 1
                    cr.gallery.content_manager.current_content_index = index

                cr.gallery.content_manager.load_contents()

                scroll_value = cr.gallery.detailed_view.thumbnail_view.scroll_value
                cr.gallery.detailed_view.thumbnail_view.reinit()
                cr.gallery.detailed_view.thumbnail_view.scroll_value = scroll_value

            self.current_result = ClipboardResultEnum.SUCCESS

        else:
            self.current_result = ClipboardResultEnum.FAILED

        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def delete(self, path: str):
        self.current_operation = ClipboardEnum.DELETE
        self.src_path = path

        self.has_popup = True
        self.current_result = ClipboardResultEnum.PENDING
        thread = threading.Thread(target=lambda: delete_file_popup(self))
        thread.start()
        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def paste(self, path: str):
        self.dst_path = path
        is_cut = self.current_operation == ClipboardEnum.CUT

        th = threading.Thread(
            target=lambda: self.__do_copy(self.src_path, self.dst_path, is_cut)
        )
        th.start()
        cr.log.write_log(self.log_text, LogLevel.ANNOUNCE)

    def save(self, path: str):
        ...

    def check_events(self):
        if self.current_result == ClipboardResultEnum.PENDING:
            if (
                self.trigger_operation
                and self.current_operation == ClipboardEnum.DELETE
            ):
                self.current_result = ClipboardResultEnum.RUNNING
                th = threading.Thread(target=lambda: self.__do_delete(self.src_path))
                th.start()
                self.trigger_operation = False

            elif (
                self.trigger_operation
                and self.current_operation == ClipboardEnum.NEW_FOLDER
            ):
                self.perform_folder_creation()
                self.trigger_operation = False
