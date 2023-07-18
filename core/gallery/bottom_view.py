from core.common.themes import ColorThemes
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.hover_man import HoverMan
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class BottomView:
    def __init__(self, box: RelRect, hover_man: HoverMan):
        self.box = box
        self.hover_man = hover_man
        self.font: Font = assets.fonts["mid"]

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

        self.fun = fun

        def make_fun(size):
            ar = utils.get_aspect_ratio(Vector2(size))

            def fun(rect):
                res = rect.copy()
                pa = self.box.get()

                res.x *= pa.w
                res.y *= pa.h
                res.w = res.h * pa.h / ar.y
                res.h *= pa.h

                res.x += pa.x
                res.y += pa.y

                return res

            return fun

        self.theme_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{cr.color_theme.current_theme.name}", True, cr.color_theme.text_0
            ),
        )

        def make_theme_box_fun():
            fun = make_fun(self.theme_text.get_rect().size)

            def new_fun(rect):
                pa = self.fun(self.theme_box.rect)
                res = fun(rect)
                res.right = pa.right
                return res

            return new_fun

        self.theme_box = RelRect(
            None,
            0.8,
            0.0,
            0.2,
            1,
            use_param=True,
        )
        self.theme_box.scale_source_function = make_theme_box_fun()

    def update_theme_text(self):
        self.theme_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{cr.color_theme.current_theme.name}", True, cr.color_theme.text_0
            ),
        )

    @property
    def theme_text_info(self):
        r1 = self.fun(self.theme_box.rect)
        s1 = self.theme_box.get()
        cut_1 = utils.cut_rect_in(r1, s1)
        src_rect_1 = utils.mult_rect(
            cut_1[1], self.theme_text.width, self.theme_text.height
        )
        return cut_1[0], src_rect_1

    def check_click(self):
        click = cr.event_holder.mouse_pressed_keys[0]
        mr = cr.event_holder.mouse_rect
        theme_rect = self.theme_text_info[0]

        if click:
            if mr.colliderect(theme_rect):
                cr.color_theme.go_next()
                self.update_theme_text()
                cr.gallery.detailed_view.top_view.sync_texts()
                cr.gallery.detailed_view.folder_view.sync_texts()
                cr.gallery.detailed_view.info_view.update_texts()

    def check_hover(self):
        mr = cr.event_holder.mouse_rect
        theme_rect = self.theme_text_info[0]

        if cr.event_holder.mouse_moved or True:
            if mr.colliderect(theme_rect):
                self.hover_man.update_text(
                    "".join([i.name + "\n" for i in cr.color_theme.ALL]), 100
                )

    def check_events(self):
        self.check_click()
        self.check_hover()

    def render(self):
        pa = self.box.get()

        info = self.theme_text_info
        self.theme_text.draw(info[1], info[0])
