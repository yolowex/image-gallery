from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets

f = FileType


class DiskCursor:
    def __init__(self):
        self.contents_dict = {}
        self.opened_content_path = None
        self.opened_content_name = None
        self.opened_content_item = None

    def init(self):
        if len(sys.argv) > 1:
            self.opened_content_path = sys.argv[1]
            self.opened_content_name = self.opened_content_path.split("/")[-1]
            print(self.opened_content_path)

        self.init_contents()

    def add_item_at(self, path: str, dict_: dict, parent_address=None):
        if not os.path.exists(path):
            # raise FileNotFoundError(f"Could not find {path}")
            cr.log.write_log(f"Could not find {path}", LogLevel.ERROR)
            return

        is_dir = os.path.isdir(path)
        is_file = os.path.isfile(path)

        if is_file:
            raise ValueError("Only directories can be added to FolderView!")

        if not is_dir and not is_file:
            # raise OSError(f"Weird item type: {path}")
            cr.log.write_log(f"Weird item type: {path}", LogLevel.ERROR)

        le = len(dict_.keys())
        name = path.split("/")[-1]

        extension = None
        meta = None
        var = name.split(".")
        if len(var) > 1:
            extension = var[-1]

        file_type = f.DIR

        address = str(le)
        if parent_address is not None:
            address = parent_address + "-" + address

        item = {
            "address": address,
            "path": path,
            "name": name,
            "extension": extension,
            "file_type": file_type,
            "meta": meta,
            "error": False,
            "is_loaded": False,
        }

        dict_[le] = item

    def add_folder(self, path: str):
        ...

    def get_item_by_address(self, address):
        keys = [int(i) for i in address.split("-")]
        item = self.contents_dict
        for i in keys:
            item = item[i]

        return item

    def expand_folder_at(self, address):
        self.expand_folder(self.get_item_by_address(address))

    def expand_folder(self, item: dict):
        item["is_loaded"] = True

        try:
            sub_items = utils.listdir(
                item["path"], include_hidden_files=False, file_type=f.DIR
            )
            sub_items.sort(key=lambda x: x.split("/")[-1].lower())
        except OSError as e:
            cr.log.write_log(
                f"Could not list all sub items of {item['path']} due to"
                f"this error: {e}",
                LogLevel.ERROR,
            )

            item["error"] = f"Error: {e}"
            return

        for sub_item in sub_items:
            self.add_item_at(sub_item, item, item["address"])

    def collapse_folder_at(self, address):
        self.collapse_folder(self.get_item_by_address(address))

    def collapse_folder(self, item: dict):
        item["is_loaded"] = False

        for i in list(item.keys()):
            if isinstance(i, int):
                del item[i]

    def init_indirect_file(self, dict_, stack):
        if not len(stack):
            return dict_

        current = stack[-1]
        failed = True
        for key in dict_:
            item = dict_[key]
            if not isinstance(item, dict):
                continue

            if current == item["path"]:
                failed = False
                stack.pop(len(stack) - 1)
                self.expand_folder(item)
                return self.init_indirect_file(item, stack)

        if failed:
            cr.log.write_log(
                f"Could not process the content root of {self.opened_content_name}",
                LogLevel.ERROR,
            )
            return False

        return dict_

    def init_contents(self):
        for path in constants.CONTENT_ROOT_LIST:
            self.add_item_at(path, self.contents_dict)

        for key in self.contents_dict:
            item = self.contents_dict[key]
            self.expand_folder(item)

        stack = []
        if self.opened_content_path is not None:
            x = self.opened_content_path.split("/")
            found_root = False
            for index, i in list(enumerate(x))[::-1]:
                path = "".join([i + "/" for i in x[:index]])[:-1]
                stack.append(path)
                if path in constants.CONTENT_ROOT_LIST:
                    found_root = True
                    break

            if not found_root:
                cr.log.write_log(
                    f"Could not find any root for {self.opened_content_path}",
                    LogLevel.ERROR,
                )
            else:
                cr.log.write_log(
                    f"Content root for {self.opened_content_name} is {stack[-1]}",
                    LogLevel.INFO,
                )

                item = self.init_indirect_file(self.contents_dict, stack)
                print("item is ", item)
                if item:
                    self.opened_content_item = item

        cr.log.write_log("Successfully initialized all content roots", LogLevel.DEBUG)
