from core.common.names import *
from core.common.enums import ClipboardEnum


class Clipboard:
    def __init__(self):
        self.current_operation: Optional[ClipboardEnum] = None
        self.src_path: Optional[str] = None
        self.dst_path: Optional[str] = None

    def copy(self, path: str):
        self.current_operation = ClipboardEnum.COPY
        self.src_path = path
        self.dst_path = None

        print("copy", self.src_path)

    def cut(self, path: str):
        self.current_operation = ClipboardEnum.CUT
        self.src_path = path
        self.dst_path = None

        print("cut", self.src_path)

    def delete(self, path: str):
        self.current_operation = ClipboardEnum.DELETE
        self.src_path = path
        print("delete", self.src_path)

    def paste(self, path: str):
        self.dst_path = path
