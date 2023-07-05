from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from helper_kit.relative_rect import RelRect
from core.common import utils

class ContentManager:
    """
    this class manages loading and unloading the contents of a directory or a search
    result.

    """

    def __init__(self,path:str=None):
        self.path: Optional[str] = path
        # stores the index number of loaded contents which reside in the content_list
        self.loaded_content_stack: list[int] = []
        self.loaded_content_stack_max_size = 100
        self.content_list: list[Content] = []
        self.current_content_index: Optional[int] = None

        self.content_load_wing = 5


    def init_contents(self):
        ...

    def load_contents(self):
        ...

    @property
    def current_content(self) -> Content:
        ...

    def check_events(self):
        ...