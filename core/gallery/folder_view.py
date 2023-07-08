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
            "name": "pic0.jpg",
            "extension": "jpg",
            "meta": None,
        },
        1: {
            "file_type": f.FILE,
            "path": None,
            "name": "pic1.png",
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
        "name": "film.mp4",
        "extension": "mp4",
        "meta": None,
    },
    4: {
        "file_type": f.FILE,
        "path": None,
        "name": "picture.jpg",
        "extension": "jpg",
        "meta": None,
    },
}



def iterate_on_flattened(dict_,function,depth=0):
    if "name" in dict_.keys():
        function(dict_,depth)
        depth += 1

    for i in dict_:
        item = dict_[i]
        if isinstance(item,dict):
            iterate_on_flattened(item,function,depth)








class FolderView:
    def __init__(self, box: RelRect, content_manager: ContentManager):
        self.box = box
        self.content_manager = content_manager
        self.font = assets.fonts['mid']

        self.text_box_list: list[tuple[Texture,RelRect]] = []


        self.item_height = 0.025
        self.indent_w = 0.1

        self.init_texts()


    def __make_fun(self,size):
        ar = utils.get_aspect_ratio(Vector2(size))
        def fun(rect) :
            res = rect.copy()
            pa = self.box.get()

            res.x += self.box.rect.x
            res.y += self.box.rect.y


            res.x *= pa.w
            res.y *= pa.h
            res.w *= (pa.h / ar.y)
            res.h *= pa.h

            return res

        return fun



    def __make_text(self,file_item:dict,depth):
        le = len(self.text_box_list)
        text = file_item["name"]
        surface = self.font.render(text,True,colors.WHITE)
        texture = Texture.from_surface(cr.renderer,surface)

        box = RelRect(
            self.__make_fun(texture.get_rect().size)
            ,self.indent_w*depth,self.item_height*le,self.item_height,self.item_height,use_param=True)

        self.text_box_list.append((texture,box))


    def init_texts(self):
        di = test_dict
        self.text_box_list.clear()
        iterate_on_flattened(di,self.__make_text)

    def check_events(self):
        ...

    def render(self):

        for text,box in self.text_box_list:
            text.draw(None,box.get())