from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class TextView:
    def __init__(self, box: RelRect, is_entry=False, text=""):
        self.font = assets.fonts["mid"]
        self.box = box
        self.text = text
        self.texture: Optional[Texture] = None
        self.is_entry = is_entry
        self.has_focus = False
        self.just_lost_focus = False

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

    def update(self, suffix=""):
        self.used_suffix = suffix != ""

        self.texture = Texture.from_surface(
            cr.renderer,
            self.font.render(" " + self.text + suffix, True, cr.color_theme.text_0),
        )

        self.main_fun = self.make_box_fun(
            self.texture, self.box, alignment=Alignment.CENTER
        )

    def check_hover(self):
        pa = self.box.get()
        mr = cr.event_holder.mouse_rect

        if pa.contains(mr):
            # unsafe / dirty
            cr.gallery.hover_man.update_text(text=self.text)

    def check_events(self):
        self.just_lost_focus = False
        self.check_hover()

        pa = self.box.get()
        mr = cr.event_holder.mouse_rect
        clicked = cr.event_holder.mouse_pressed_keys[0]
        any_clicked = any(cr.event_holder.mouse_pressed_keys)
        right_clicked = cr.event_holder.mouse_pressed_keys[2]

        if clicked:
            if pa.contains(mr):
                self.has_focus = True

        if any_clicked:
            if not pa.contains(mr):
                self.has_focus = False
                self.just_lost_focus = True

        if right_clicked:
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
                if i.type == pgl.KEYDOWN:
                    char = i.unicode
                    if char in constants.SUPPORTED_CHARACTERS:
                        self.text += char
                        self.update()

                    if i.key == pgl.K_BACKSPACE:
                        self.text = self.text[:-1]
                        if (
                            pgl.K_LCTRL in cr.event_holder.held_keys
                            or pgl.K_RCTRL in cr.event_holder.held_keys
                        ):
                            self.text = ""
                        self.update()

    def render(self):
        cr.renderer.draw_color = cr.color_theme.color_2
        cr.renderer.draw_rect(self.box.get())

        self.texture.draw(None, self.main_fun(self.box.rect))
