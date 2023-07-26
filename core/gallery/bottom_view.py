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

        self.announce_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{cr.log.last_announcement}", True, cr.color_theme.text_0
            ),
        )

        def make_box_fun(text: Texture, box: RelRect, alignment: Alignment = None):
            fun = make_fun(text.get_rect().size)

            def new_fun(rect):
                pa = self.fun(box.rect)
                res = fun(rect)

                if alignment == Alignment.CENTER:
                    res.center = pa.center
                elif alignment == Alignment.LEFT:
                    res.left = pa.left
                elif alignment == Alignment.RIGHT:
                    res.right = pa.right

                return res

            return new_fun

        self.make_box_fun = make_box_fun

        self.announce_box = RelRect(
            None,
            0.2,
            0.0,
            0.6,
            1,
            use_param=True,
        )
        self.announce_box.scale_source_function = make_box_fun(
            self.announce_text, self.announce_box, alignment=Alignment.LEFT
        )

        self.theme_box = RelRect(
            None,
            0.8,
            0.0,
            0.2,
            1,
            use_param=True,
        )
        self.theme_box.scale_source_function = make_box_fun(
            self.theme_text, self.theme_box, Alignment.RIGHT
        )

    def update_theme_text(self):
        self.theme_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{cr.color_theme.current_theme.name}", True, cr.color_theme.text_0
            ),
        )
        self.theme_box = RelRect(
            None,
            0.8,
            0.0,
            0.2,
            1,
            use_param=True,
        )
        self.theme_box.scale_source_function = self.make_box_fun(
            self.theme_text, self.theme_box, Alignment.RIGHT
        )

    def update_announce_text(self):
        self.announce_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{cr.log.last_announcement}", True, cr.color_theme.text_0
            ),
        )
        self.announce_box = RelRect(
            None,
            0.2,
            0.0,
            0.6,
            1,
            use_param=True,
        )
        self.announce_box.scale_source_function = self.make_box_fun(
            self.announce_text, self.announce_box, alignment=Alignment.LEFT
        )

    def get_info(self, text: Texture, box: RelRect):
        r1 = self.fun(box.rect)
        s1 = box.get()
        cut_1 = utils.cut_rect_in(r1, s1)
        src_rect_1 = utils.mult_rect(cut_1[1], text.width, text.height)
        return cut_1[0], src_rect_1

    def check_click(self):
        theme_info = self.get_info(self.theme_text, self.theme_box)
        click = cr.event_holder.mouse_pressed_keys[0]
        mr = cr.event_holder.mouse_rect
        theme_rect = theme_info[0]

        if click:
            if mr.colliderect(theme_rect):
                cr.color_theme.go_next()
                self.update_theme_text()
                self.update_announce_text()
                cr.gallery.detailed_view.top_view.sync_texts()
                cr.gallery.detailed_view.tag_view.load()
                cr.gallery.detailed_view.folder_view.sync_texts()
                cr.gallery.detailed_view.info_view.update_texts()

    def check_hover(self):
        theme_info = self.get_info(self.theme_text, self.theme_box)
        ann_info = self.get_info(self.announce_text, self.announce_box)

        mr = cr.event_holder.mouse_rect
        theme_rect = theme_info[0]

        ann_rect = ann_info[0]

        if mr.colliderect(theme_rect):
            self.hover_man.update_text(
                "".join([i.name + "\n" for i in cr.color_theme.ALL]), 100
            )

        if mr.colliderect(ann_rect):
            self.hover_man.update_text(cr.log.last_announcement, 100)

    def check_events(self):
        self.check_click()
        self.check_hover()
        if cr.log.was_updated:
            # unsafe af
            cr.log.was_updated = False
            self.update_announce_text()

    def render(self):
        pa = self.box.get()

        theme_info = self.get_info(self.theme_text, self.theme_box)
        ann_info = self.get_info(self.announce_text, self.announce_box)

        self.theme_text.draw(theme_info[1], theme_info[0])
        self.announce_text.draw(ann_info[1], ann_info[0])
