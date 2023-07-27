from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.name_tag import NameTag
from gui.text_view import TextView
from gui.zoom_view import ZoomView
from helper_kit.relative_pos import RelPos
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


class EditView:
    def __init__(self, box: RelRect):
        self.box = box
        self.font: Font = assets.fonts["mid"]
        self.vertical_margin = 0.01
        self.height_counter = 0

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

        self.text_view_list: list[TextView] = []
        self.button_list: list[Button] = []

        self.init_contents()

    def init_contents(self):
        self.add_tv_button(assets.ui_buttons["edit_flip_x"], "Mirror", "Mirror")
        self.add_tv_button(
            assets.ui_buttons["edit_rotate_right"], "Rotate Right", "Rotate Right"
        )
        self.add_tv_button(
            assets.ui_buttons["edit_rotate_left"], "Rotate Left", "Rotate Left"
        )

        self.add_effect_tv_row(["Vintage", "High Contrast"])
        self.add_effect_tv_row(
            [
                "HDR",
                "Sepia Tone",
            ]
        )
        self.add_effect_tv_row(["Soft Focus", "Pop Art"])
        self.add_effect_tv_row(["Glow Effect"])
        self.add_effect_tv_row(["Cross Processing"])
        self.add_effect_tv_row(["Solarization", "Comic Book"])
        self.add_effect_tv_row(["Tilt Shift", "Pencil Sketch"])

    def add_effect_tv_row(self, texts: list[str]):
        height = 0.05

        y = 0.01 + (self.height_counter * (height + self.vertical_margin))

        # unsafe: this will raise an error if texts is empty
        step_w = 0.99 / len(texts)

        for index, text in enumerate(texts):
            tv_box = RelRect(
                self.fun, 0.01 + step_w * index, y, step_w, height, use_param=True
            )
            tv = TextView(tv_box, is_entry=False, text=text)

            self.text_view_list.append(tv)

        self.height_counter += 1

    def add_tv_button(
        self,
        button_texture: Texture,
        button_name: str,
        text="",
        has_focus=True,
    ):
        height = 0.05

        y = 0.01 + (self.height_counter * (height + self.vertical_margin))

        tv_box = RelRect(self.fun, 0.01, y, 0.8, height, use_param=True)
        tv = TextView(tv_box, is_entry=False, text=text)
        tv.has_focus = has_focus
        tv_button_box = RelRect(self.button_fun, 0.8, y, 0.2, height, use_param=True)

        tv_button = Button(
            button_name,
            tv_button_box,
            button_texture,
            cr.mouse.enable_virtual,
            None,
        )

        self.text_view_list.append(tv)
        self.button_list.append(tv_button)
        #
        # self.sync_location_text()

        self.height_counter += 1

    def check_events(self):
        for text_view in self.text_view_list:
            text_view.check_events()

        for button in self.button_list:
            button.check_events()

    def render(self):
        cr.renderer.draw_rect(self.box.get())

        for text_view in self.text_view_list:
            text_view.render()

        for button in self.button_list:
            button.render()
