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
        self.init_contents()


    def add_item_at(self, path: str, dict_: dict, parent_address=None):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Could not find {path}")

        is_dir = os.path.isdir(path)
        is_file = os.path.isfile(path)

        if not is_dir and not is_file:
            raise OSError(f"Weird item type: {path}")

        le = len(dict_.keys())
        name = path.split("/")[-1]

        extension = None
        meta = None
        var = name.split(".")
        if len(var) > 1:
            extension = var[-1]

        file_type = f.FILE
        if is_dir:
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
        }

        if is_dir:
            item["is_loaded"] = False

        dict_[le] = item

    def add_folder(self, path: str):
        ...

    def expand_folder(self, item: dict):
        sub_items = utils.listdir(item["path"],include_hidden_files=False)

        for sub_item in sub_items:
            self.add_item_at(sub_item,item,item['address'])


    def collapse_folder(self, item: dict):
        ...

    def init_contents(self):
        for path in constants.CONTENT_ROOT_LIST:
            self.add_item_at(path, self.contents_dict)

        for key in self.contents_dict:
            item = self.contents_dict[key]

            if item["file_type"] == f.DIR:
                self.expand_folder(item)

        print(self.contents_dict)
