from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.name_tag import NameTag
from gui.spectrum import Spectrum
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
        self.item_height = 0.05
        self.height_counter = 0
        self.scroll_y = 0
        self.scroll_x_locked = False

        def fun(rect):
            # win_size = cr.ws()
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y + self.scroll_y * self.content_height * pa.h
            return res

        def button_fun(rect):
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y + self.scroll_y * self.content_height * pa.h
            lc = res.center
            res.w = res.h
            res.center = lc
            return res

        self.fun = fun
        self.button_fun = button_fun

        self.text_view_list: list[TextView] = []
        self.button_list: list[Button] = []
        self.spectrum_list: list[Spectrum] = []

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

        self.add_spectrum(
            assets.ui_buttons["edit_brightness"], lambda: print("brightness"), 1.25
        )
        self.add_spectrum(
            assets.ui_buttons["edit_contrast"], lambda: print("contrast"), 1.25
        )
        self.add_spectrum(
            assets.ui_buttons["edit_sharpness"], lambda: print("sharpness"), 1.25
        )

        self.add_spectrum(assets.ui_buttons["edit_red"], lambda: print("red"), 1)
        self.add_spectrum(assets.ui_buttons["edit_green"], lambda: print("green"), 1)
        self.add_spectrum(assets.ui_buttons["edit_blue"], lambda: print("blue"), 1)
        self.add_spectrum(
            assets.ui_buttons["edit_saturation"], lambda: print("saturation"), 1.25
        )
        self.add_spectrum(
            assets.ui_buttons["edit_shadow"], lambda: print("shadow"), 1.25
        )
        self.add_spectrum(
            assets.ui_buttons["edit_highlight"], lambda: print("highlight"), 1.25
        )

        self.add_effect_tv_row(["Abort", "Save"])

    def add_spectrum(self, button_texture: Texture, source_function, y_scale=1.0):
        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))
        tv_box = RelRect(self.fun, 0.05, y, 0.75, self.item_height, use_param=True)

        spectrum = Spectrum(tv_box, button_texture, source_function, y_scale)

        tv_button_box = RelRect(
            self.button_fun, 0.8, y, 0.2, self.item_height, use_param=True
        )

        def func():
            spectrum.scroll_value = 0.5
            spectrum.on_release_function()

        tv_button = Button(
            "Reset",
            tv_button_box,
            assets.ui_buttons["reset"],
            func,
            None,
        )
        self.spectrum_list.append(spectrum)
        self.button_list.append(tv_button)
        self.height_counter += 1

    def add_effect_tv_row(self, texts: list[str]):
        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))

        # unsafe: this will raise an error if texts is empty
        step_w = 0.93 / len(texts)

        for index, text in enumerate(texts):
            tv_box = RelRect(
                self.fun,
                0.05 + step_w * index,
                y,
                step_w,
                self.item_height,
                use_param=True,
            )
            tv = TextView(tv_box, is_entry=False, text=text, y_scale=0.65)

            self.text_view_list.append(tv)

        self.height_counter += 1

    def add_tv_button(
        self,
        button_texture: Texture,
        button_name: str,
        text="",
        has_focus=True,
    ):
        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))

        tv_box = RelRect(self.fun, 0.05, y, 0.75, self.item_height, use_param=True)
        tv = TextView(tv_box, is_entry=False, text=text, y_scale=0.8)
        tv.has_focus = has_focus
        tv_button_box = RelRect(
            self.button_fun, 0.8, y, 0.2, self.item_height, use_param=True
        )

        tv_button = Button(
            button_name,
            tv_button_box,
            button_texture,
            lambda: None,
            None,
        )

        self.text_view_list.append(tv)
        self.button_list.append(tv_button)
        #
        # self.sync_location_text()

        self.height_counter += 1

    @property
    def __vertical_scroll_bar_width(self):
        pa = self.box.get()

        val = cr.ws().y * 0.01
        if val > pa.h * 0.1:
            val = pa.h * 0.1

        return val

    @property
    def __vertical_scroll_bar_rect(self):
        pa = self.box.get()
        w = self.__vertical_scroll_bar_width
        y = pa.y
        x = pa.left
        h = pa.h

        return FRect(x, y, w, h)

    @property
    def content_height(self):
        return self.height_counter * (self.item_height + self.vertical_margin)

    @property
    def __vertical_scroll_button_rect(self):
        pa = self.box.get()
        bar_rect = self.__vertical_scroll_bar_rect

        bottom_bound = -self.content_height + 0.95

        h = self.box.rect.h / self.content_height * pa.h

        if h > pa.h:
            h = pa.h

        lerp_value = utils.inv_lerp(0, abs(bottom_bound), abs(self.scroll_y))

        rect = FRect(
            bar_rect.x,
            utils.lerp(bar_rect.top, bar_rect.bottom - h, lerp_value),
            bar_rect.w,
            h,
        )

        return rect

    def check_scroll_bar(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = Vector2(mr.center)
        mod = pgl.K_LCTRL in cr.event_holder.held_keys
        clicked = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]

        if mr.colliderect(pa):
            if mw:
                self.scroll_y += mw * 0.04
                if self.scroll_y > 0:
                    self.scroll_y = 0
                bottom_bound = -self.content_height + 0.95
                if self.scroll_y < bottom_bound:
                    self.scroll_y = bottom_bound

        if clicked:
            v_bar = self.__vertical_scroll_bar_rect

            if mr.colliderect(v_bar):
                self.scroll_x_locked = True

        if released:
            self.scroll_x_locked = False

        if self.scroll_x_locked:
            bar = self.__vertical_scroll_bar_rect
            bottom_bound = -self.content_height + 0.95
            val = utils.inv_lerp(bar.top, bar.bottom, mp.y)
            self.scroll_y = utils.lerp(0, bottom_bound, val)
            if self.scroll_y > 0:
                self.scroll_y = 0
            if self.scroll_y < bottom_bound:
                self.scroll_y = bottom_bound

        if self.content_height < 1:
            self.scroll_y = 0

    def check_events(self):
        self.check_scroll_bar()

        for text_view in self.text_view_list:
            text_view.check_events()

        for button in self.button_list:
            button.check_events()

        for spectrum in self.spectrum_list:
            spectrum.check_events()

    def render(self):
        cr.renderer.draw_rect(self.box.get())

        for text_view in self.text_view_list:
            text_view.render()

        for spectrum in self.spectrum_list:
            spectrum.render()

        for button in self.button_list:
            button.render()

        cr.renderer.draw_color = cr.color_theme.color_0
        cr.renderer.fill_rect(self.__vertical_scroll_bar_rect)

        cr.renderer.draw_color = cr.color_theme.scroll_bar_border
        cr.renderer.draw_rect(self.__vertical_scroll_bar_rect)

        cr.renderer.draw_color = cr.color_theme.button
        cr.renderer.fill_rect(self.__vertical_scroll_button_rect)
