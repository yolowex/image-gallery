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
            # raise FileNotFoundError(f"Could not find {path}")
            cr.log.write_log(f"Could not find {path}",LogLevel.ERROR)
            return

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
            "error":False
        }

        if is_dir:
            item["is_loaded"] = False

        dict_[le] = item

    def add_folder(self, path: str):
        ...

    def get_item_by_address(self,address):
        keys = [int(i) for i in address.split("-")]
        item = self.contents_dict
        for i in keys :
            item = item[i]

        return item

    def expand_folder_at(self,address):
        self.expand_folder(self.get_item_by_address(address))

    def expand_folder(self, item: dict):
        item['is_loaded'] = True

        try:
            sub_items = utils.listdir(item["path"],include_hidden_files=False)
            sub_items.sort(key=lambda x: x.split("/")[-1].lower())
        except OSError as e:
            cr.log.write_log(f"Could not list all sub items of {item['path']} due to"
                        f"this error: {e}",LogLevel.ERROR)

            item['error'] = f"Error: {e}"
            return

        for sub_item in sub_items :
            self.add_item_at(sub_item, item, item['address'])





    def collapse_folder_at(self,address):
        self.collapse_folder(self.get_item_by_address(address))

    def collapse_folder(self, item: dict):
        item['is_loaded'] = False

        for i in list(item.keys()):
            if isinstance(i,int):
                del(item[i])



    def init_contents(self):
        for path in constants.CONTENT_ROOT_LIST:
            self.add_item_at(path, self.contents_dict)

        for key in self.contents_dict:
            item = self.contents_dict[key]

            if item["file_type"] == f.DIR:
                self.expand_folder(item)

        cr.log.write_log("Successfully initialized all content roots",LogLevel.DEBUG)
