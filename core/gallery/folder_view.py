from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


f = FileType

test_dict = {
    0: {
        "file_type": f.DIR,
        "path": None,
        "name": "pics",
        "extension": None,
        "meta": None,
        0: {
            "file_type": f.FILE,
            "path": None,
            "name": "pic0",
            "extension": "jpg",
            "meta": None,
        },
        1: {
            "file_type": f.FILE,
            "path": None,
            "name": "pic1",
            "extension": "png",
            "meta": None,
        },
    },
    1: {
        "file_type": f.DIR,
        "path": None,
        "name": "folder",
        "extension": None,
        "meta": None,
        0: {
            "file_type": f.DIR,
            "path": None,
            "name": "folder",
            "extension": None,
            "meta": None,
            0: {
                "file_type": f.DIR,
                "path": None,
                "name": "folder",
                "extension": None,
                "meta": None,
            },
        },
    },
    2: {
        "file_type": f.DIR,
        "path": None,
        "name": "music",
        "extension": None,
        "meta": None,
    },
    3: {
        "file_type": f.FILE,
        "path": None,
        "name": "film",
        "extension": "mp4",
        "meta": None,
    },
    4: {
        "file_type": f.FILE,
        "path": None,
        "name": "picture",
        "extension": "jpg",
        "meta": None,
    },
}


class FolderView:
    def __init__(self, box: RelRect, content_manager: ContentManager):
        self.box = box
        self.content_manager = content_manager

    def check_events(self):
        ...

    def render(self):
        ...
