from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class TextView:
    def __init__(
        self,
        box: RelRect,
        is_entry=False,
        text="",
        y_scale=1,
        on_click_function=None,
        line_max_char=None,
    ):
        self.on_click_function = on_click_function
        self.font = assets.fonts["mid"]
        self.box = box
        self.text = text
        self.texture: Optional[Texture] = None
        self.y_scale = y_scale
        self.is_entry = is_entry
        self.has_focus = False
        self.just_lost_focus = False
        self.line_max_char: Optional[int] = line_max_char
        self.total_lines = 1

        self.cursor_timer = utils.now()
        self.cursor_duration = 0.6
        self.used_suffix = False

        def make_fun(size):
            ar = utils.get_aspect_ratio(Vector2(size))

            def fun(rect):
                res = rect.copy()
                pa = self.box.get()

                res.x = pa.x
                res.y = pa.y
                res.h = pa.h
                res.w = pa.h / ar.y

                return res

            return fun

        def make_box_fun(text: Texture, box: RelRect, alignment: Alignment = None):
            fun = make_fun(text.get_rect().size)

            def new_fun(rect):
                pa = box.get()
                res = fun(rect)
                res.h *= self.y_scale * self.total_lines
                res.w *= self.y_scale * self.total_lines

                # dirty: redundant
                res.center = pa.center
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

        self.make_box_fun = make_box_fun
        self.main_fun = None

        self.update()

    def get_info(self, text: Texture, box: RelRect):
        s1 = self.main_fun(box.rect)
        r1 = box.get()
        cut_1 = utils.cut_rect_in(r1, s1)
        src_rect_1 = utils.mult_rect(cut_1[1], text.width, text.height)
        return cut_1[0], src_rect_1

    def update(self, suffix=""):
        self.total_lines = 1
        self.used_suffix = suffix != ""
        text = self.text

        new_text = ""
        if self.line_max_char is None:
            new_text = text
        else:
            c = 0
            for i in text:
                c += 1

                if c == self.line_max_char:
                    new_text += "\n"
                    c = 0
                    self.total_lines += 1

                new_text += i

        self.texture = Texture.from_surface(
            cr.renderer,
            self.font.render(" " + new_text + suffix, True, cr.color_theme.text_0),
        )

        self.main_fun = self.make_box_fun(
            self.texture, self.box, alignment=Alignment.CENTER
        )

    def check_hover(self):
        pa = self.box.get()
        mr = cr.event_holder.mouse_rect

        if pa.contains(mr) and self.text != "":
            # unsafe / dirty
            cr.gallery.hover_man.update_text(text=self.text)

    def check_click(self):
        if callable(self.on_click_function):
            mr = cr.event_holder.mouse_rect
            pressed = cr.event_holder.mouse_pressed_keys[0]

            if pressed and self.box.get().contains(mr):
                self.on_click_function()

    def check_events(self):
        self.just_lost_focus = False
        self.check_hover()
        self.check_click()
        pa = self.box.get()
        mr = cr.event_holder.mouse_rect
        clicked = cr.event_holder.mouse_pressed_keys[0]
        any_clicked = any(cr.event_holder.mouse_pressed_keys)
        right_clicked = cr.event_holder.mouse_pressed_keys[2]

        if clicked:
            if pa.contains(mr):
                self.has_focus = True
            elif self.has_focus:
                self.has_focus = False
                self.just_lost_focus = True

        elif self.has_focus:
            if right_clicked:
                self.has_focus = False
                self.just_lost_focus = True

            elif any_clicked:
                if not pa.contains(mr):
                    self.has_focus = False
                    self.just_lost_focus = True

        if any_clicked:
            self.update()

        if self.has_focus and self.is_entry:
            if utils.now() > self.cursor_timer + self.cursor_duration:
                self.cursor_timer = utils.now()
                if self.used_suffix:
                    self.update()
                else:
                    self.update("|")

            for i in cr.event_holder.events:
                if i.type == pgl.TEXTINPUT:
                    char = i.text

                    if char in constants.SUPPORTED_CHARACTERS:
                        self.text += char
                        self.update()

                if i.type == pgl.KEYDOWN:
                    if i.key == pgl.K_RETURN:
                        self.has_focus = False
                        self.just_lost_focus = True
                        self.update()
                        return

                    if i.key == pgl.K_BACKSPACE:
                        self.text = self.text[:-1]
                        if (
                            pgl.K_LCTRL in cr.event_holder.held_keys
                            or pgl.K_RCTRL in cr.event_holder.held_keys
                        ):
                            self.text = ""
                        self.update()

    @property
    def bg_color(self):
        mr = cr.event_holder.mouse_rect
        pressed = cr.event_holder.mouse_pressed_keys[0]
        held = cr.event_holder.mouse_held_keys[0]

        if self.box.get().contains(mr):
            if held:
                return cr.color_theme.color_1.lerp(cr.color_theme.selection, 0.5)
            else:
                return cr.color_theme.color_1.lerp(cr.color_theme.selection, 0.15)

        return cr.color_theme.color_1

    def render(self):
        cr.renderer.draw_color = self.bg_color
        cr.renderer.fill_rect(self.box.get())

        cr.renderer.draw_color = cr.color_theme.color_2
        cr.renderer.draw_rect(self.box.get())

        info = self.get_info(self.texture, self.box)
        self.texture.draw(info[1], info[0])
