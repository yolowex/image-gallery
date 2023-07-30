import copy

from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.edit_agent import EditAgent
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

    @property
    def edit_agent(self) -> EditAgent:
        content: Content = cr.gallery.content_manager.current_content

        return content.edit_agent

    def sync_edits(self):
        content: Content = cr.gallery.content_manager.current_content

        if content.type == ContentType.PICTURE:
            content.edit_agent.perform()

    def get_spectrum(self, name) -> Optional[Spectrum]:
        for spectrum in self.spectrum_list:
            if spectrum.name == name:
                return spectrum

        return None

    def sync_spectrums(self):
        ea = self.edit_agent
        self.get_spectrum("brightness").scroll_value = ea.brightness
        self.get_spectrum("contrast").scroll_value = ea.contrast
        self.get_spectrum("sharpness").scroll_value = ea.sharpness
        self.get_spectrum("saturation").scroll_value = ea.saturation
        self.get_spectrum("red").scroll_value = ea.red
        self.get_spectrum("green").scroll_value = ea.green
        self.get_spectrum("blue").scroll_value = ea.blue

    def init_contents(self):
        def flip_function():
            self.edit_agent.flip_x = not self.edit_agent.flip_x
            self.edit_agent.perform()

        def rotate_right_function():
            self.edit_agent.angle -= 90
            self.edit_agent.perform()

        def rotate_left_function():
            self.edit_agent.angle += 90
            self.edit_agent.perform()

        self.add_tv_button(
            assets.ui_buttons["edit_flip_x"],
            "Mirror",
            "Mirror",
            on_click_function=flip_function,
        )
        self.add_tv_button(
            assets.ui_buttons["edit_rotate_right"],
            "Rotate Right",
            "Rotate Right",
            on_click_function=rotate_right_function,
        )
        self.add_tv_button(
            assets.ui_buttons["edit_rotate_left"],
            "Rotate Left",
            "Rotate Left",
            on_click_function=rotate_left_function,
        )

        def black_and_white_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0
            self.edit_agent.brightness = 0.25
            self.edit_agent.contrast = 0.7
            self.sync_spectrums()
            self.edit_agent.perform()

        def cozy_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.7
            self.edit_agent.brightness = 0.3
            self.edit_agent.contrast = 0.3
            self.edit_agent.sharpness = 0.8
            self.edit_agent.red = 0.75
            self.edit_agent.blue = 0.5
            self.edit_agent.green = 0.6
            self.sync_spectrums()
            self.edit_agent.perform()

        def fog_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.3
            self.edit_agent.brightness = 0.5
            self.edit_agent.contrast = 0.25
            self.edit_agent.sharpness = 0.15
            self.edit_agent.red = 0.5
            self.edit_agent.blue = 0.8
            self.edit_agent.green = 0.5
            self.sync_spectrums()
            self.edit_agent.perform()

        def inferno_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.35
            self.edit_agent.brightness = 0.7
            self.edit_agent.contrast = 0.6
            self.edit_agent.sharpness = 0.75
            self.edit_agent.red = 0.65
            self.edit_agent.blue = 0.35
            self.edit_agent.green = 0.35
            self.sync_spectrums()
            self.edit_agent.perform()

        def blue_dust_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.35
            self.edit_agent.brightness = 0.7
            self.edit_agent.contrast = 0.6
            self.edit_agent.sharpness = 0.75
            self.edit_agent.red = 0.35
            self.edit_agent.blue = 0.65
            self.edit_agent.green = 0.35
            self.sync_spectrums()
            self.edit_agent.perform()

        def forest_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.3
            self.edit_agent.brightness = 0.5
            self.edit_agent.contrast = 0.30
            self.edit_agent.sharpness = 0.20
            self.edit_agent.red = 0.55
            self.edit_agent.blue = 0.4
            self.edit_agent.green = 0.8
            self.sync_spectrums()
            self.edit_agent.perform()

        def vintage_function():
            self.edit_agent.reset_effects()
            self.edit_agent.saturation = 0.2
            self.edit_agent.brightness = 0.45
            self.edit_agent.contrast = 0.15
            self.edit_agent.sharpness = 0.7
            self.edit_agent.red = 0.55
            self.edit_agent.blue = 0.3
            self.edit_agent.green = 0.4
            self.sync_spectrums()
            self.edit_agent.perform()

        self.add_effect_tv_row(["Black And White"], [black_and_white_function])
        self.add_effect_tv_row(["Inferno"], [inferno_function])
        self.add_effect_tv_row(["Cold Fog", "Forest"], [fog_function, forest_function])
        self.add_effect_tv_row(
            ["Desert", "Blue Dust"], [cozy_function, blue_dust_function]
        )
        self.add_effect_tv_row(["Vintage"], [vintage_function])

        def make_brightness_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.brightness = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_contrast_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.contrast = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_saturation_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.saturation = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_sharpness_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.sharpness = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_red_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.red = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_green_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.green = spectrum.scroll_value
                self.sync_edits()

            return fun

        def make_blue_fun(spectrum: Spectrum):
            def fun():
                self.edit_agent.blue = spectrum.scroll_value
                self.sync_edits()

            return fun

        self.add_spectrum(
            assets.ui_buttons["edit_brightness"],
            make_brightness_fun,
            1.25,
            name="brightness",
        )
        self.add_spectrum(
            assets.ui_buttons["edit_contrast"], make_contrast_fun, 1.25, name="contrast"
        )
        self.add_spectrum(
            assets.ui_buttons["edit_sharpness"],
            make_sharpness_fun,
            1.25,
            name="sharpness",
        )

        self.add_spectrum(assets.ui_buttons["edit_red"], make_red_fun, 1, name="red")
        self.add_spectrum(
            assets.ui_buttons["edit_green"], make_green_fun, 1, name="green"
        )
        self.add_spectrum(assets.ui_buttons["edit_blue"], make_blue_fun, 1, name="blue")
        self.add_spectrum(
            assets.ui_buttons["edit_saturation"],
            make_saturation_fun,
            1.25,
            name="saturation",
        )

        self.add_effect_tv_row(["Reset", "Save"], [self.reset, self.save])

    def add_spectrum(self, button_texture: Texture, function, y_scale=1.0, name=""):
        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))
        tv_box = RelRect(self.fun, 0.05, y, 0.75, self.item_height, use_param=True)

        spectrum = Spectrum(tv_box, button_texture, lambda: None, y_scale, name=name)
        spectrum.on_release_function = function(spectrum)

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

    def add_effect_tv_row(self, texts: list[str], functions: list = None):
        if functions is None:
            return

        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))

        # unsafe: this will raise an error if texts is empty
        step_w = 0.93 / len(texts)

        for index, text, function in zip(range(len(texts)), texts, functions):
            tv_box = RelRect(
                self.fun,
                0.05 + step_w * index,
                y,
                step_w,
                self.item_height,
                use_param=True,
            )
            tv = TextView(
                tv_box,
                is_entry=False,
                text=text,
                y_scale=0.65,
                on_click_function=function,
            )

            self.text_view_list.append(tv)

        self.height_counter += 1

    def add_tv_button(
        self,
        button_texture: Texture,
        button_name: str,
        text="",
        has_focus=True,
        on_click_function=None,
    ):
        y = 0.01 + (self.height_counter * (self.item_height + self.vertical_margin))

        tv_box = RelRect(self.fun, 0.05, y, 0.75, self.item_height, use_param=True)
        tv = TextView(
            tv_box,
            is_entry=False,
            text=text,
            y_scale=0.8,
            on_click_function=on_click_function,
        )
        tv.has_focus = has_focus
        tv_button_box = RelRect(
            self.button_fun, 0.8, y, 0.2, self.item_height, use_param=True
        )

        tv_button = Button(
            button_name,
            tv_button_box,
            button_texture,
            on_click_function,
            None,
        )

        self.text_view_list.append(tv)
        self.button_list.append(tv_button)
        #
        # self.sync_location_text()

        self.height_counter += 1

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

    def reset(self):
        self.edit_agent.reset_everything()
        self.sync_spectrums()
        self.edit_agent.perform()

    def save(self):
        content: Content = cr.gallery.content_manager.current_content

        name = content.name
        pure_name = content.pure_name
        extension = content.extension
        dst_path = cr.gallery.content_manager.path
        c = 0
        while True:
            this_name = pure_name

            if c != 0:
                this_name += f"_{c}"

            this_name += "." + extension

            path = pathlib.Path(dst_path + "/" + this_name).resolve().as_posix()
            if not os.path.exists(path):
                break

            c += 1

        content.modified_image.save(path)
        cr.gallery.content_manager.reinit()
        cr.gallery.detailed_view.thumbnail_view.reinit()
