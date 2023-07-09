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

test_dict = {}


def make_test_dict(dict_, depth=0):
    mx = 5
    d = depth + 1
    if depth >= mx: d = mx

    egg = random.randint(d,mx)

    if depth >= mx: return

    for i in range(egg):
        t = random.choice([f.FILE, f.DIR, f.DIR, f.DIR])

        item = {
            "name": f"{t.name.lower()}-{i}-{depth}",
            "file_type": t}
        dict_[i] = item

        if item["file_type"] == f.DIR:
            make_test_dict(item,depth+1)

make_test_dict(test_dict)



def iterate_on_flattened(dict_, function, depth=0):
    if "name" in dict_.keys():
        function(dict_, depth)
        depth += 1

    for i in dict_:
        item = dict_[i]
        if isinstance(item, dict):
            iterate_on_flattened(item, function, depth)


class FolderView:
    def __init__(self, box: RelRect, content_manager: ContentManager):
        self.box = box
        self.content_manager = content_manager
        self.font = assets.fonts["mid"]

        self.text_box_list: list[tuple[Texture, RelRect]] = []

        self.item_height = 0.025
        self.indent_w = 0.045

        self.init_texts()

    def __make_fun(self, size):
        ar = utils.get_aspect_ratio(Vector2(size))

        def fun(rect):
            res = rect.copy()
            pa = self.box.get()

            res.x += self.box.rect.x
            res.y += self.box.rect.y

            res.x *= pa.h
            res.y *= pa.h
            res.w *= pa.h / ar.y
            res.h *= pa.h

            return res

        return fun

    def __make_text(self, file_item: dict, depth):
        le = len(self.text_box_list)
        text = file_item["name"]
        surface = self.font.render(text, True, colors.WHITE)
        texture = Texture.from_surface(cr.renderer, surface)

        box = RelRect(
            self.__make_fun(texture.get_rect().size),
            self.indent_w * depth,
            self.item_height * le,
            self.item_height,
            self.item_height,
            use_param=True,
        )

        self.text_box_list.append((texture, box))

    def init_texts(self):
        di = test_dict
        self.text_box_list.clear()
        iterate_on_flattened(di, self.__make_text)

    def check_events(self):
        ...

    def render(self):
        for text, box in self.text_box_list:
            text.draw(None, box.get())
