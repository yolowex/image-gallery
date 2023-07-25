from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.text_view import TextView
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


def make_fun(size, con_box):
    ar = utils.get_aspect_ratio(Vector2(size))

    def fun(rect):
        res = rect.copy()
        pa = con_box.get()

        res.x = pa.x
        res.y = pa.y
        res.h = pa.h
        res.w = pa.h / ar.y
        return res

    return fun


def make_box_fun(
    text: Texture, box: RelRect, alignment: Alignment = None, con_box=None
):
    fun = make_fun(text.get_rect().size, con_box)

    def new_fun(rect):
        pa = box.get()
        res = fun(rect)
        if alignment == Alignment.CENTER:
            res.center = pa.center
        elif alignment == Alignment.LEFT:
            res.left = pa.left
        elif alignment == Alignment.RIGHT:
            res.right = pa.right

        if res.right > pa.right:
            res.right = pa.right

        return res

    return new_fun


class TagView:
    def __init__(self, box: RelRect):
        self.box = box
        self.font: Font = assets.fonts["mid"]
        self.people_text_view_list: list[TextView] = []
        self.people_button_list: list[Button] = []

        def fun(rect):
            # win_size = cr.ws()
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y
            return res

        def button_fun(rect):
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y

            lc = res.center
            res.w = res.h
            res.center = lc
            return res

        self.fun = fun
        self.button_fun = button_fun

        self.people_box = RelRect(fun, 0.01, 0.01, 0.8, 0.05, use_param=True)
        self.people_text = TextView(self.people_box, is_entry=False, text="Add People")
        self.add_people_box = RelRect(button_fun, 0.8, 0.01, 0.2, 0.05, use_param=True)

        self.add_people_button = Button(
            "Add People",
            self.add_people_box,
            assets.ui_buttons["tag_add"],
            self.add_person,
            None,
        )

    def add_person(self):
        height = 0.05
        vertical_margin = 0.001
        y = 0.01 + (1 + len(self.people_text_view_list)) * (height + vertical_margin)

        person_box = RelRect(self.fun, 0.01, y, 0.8, height, use_param=True)
        person_text = TextView(person_box, is_entry=True, text="")
        person_text.has_focus = True
        move_person_box = RelRect(self.button_fun, 0.8, y, 0.2, height, use_param=True)

        move_person_button = Button(
            "Move Box",
            move_person_box,
            assets.ui_buttons["tag_move"],
            lambda: print("oy yes"),
            None,
        )

        self.people_text_view_list.append(person_text)
        self.people_button_list.append(move_person_button)

    def check_events(self):
        self.people_text.check_events()
        for text_view in self.people_text_view_list:
            text_view.check_events()

        for index, text_view in list(enumerate(self.people_text_view_list))[::-1]:
            if text_view.just_lost_focus and text_view.text == "":
                self.people_text_view_list.pop(index)
                self.people_button_list.pop(index)

        self.add_people_button.check_events()

        for button in self.people_button_list:
            button.check_events()

    def render(self):
        cr.renderer.draw_rect(self.box.get())
        self.people_text.render()
        self.add_people_button.render()

        for text_view in self.people_text_view_list:
            text_view.render()

        for button in self.people_button_list:
            button.render()
