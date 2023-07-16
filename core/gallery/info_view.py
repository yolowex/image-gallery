from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class InfoView:
    def __init__(self, box: RelRect):
        self.box = box
        self.font: Font = assets.fonts["mid"]

        def fun(rect):
            res = rect.copy()
            pa = self.box.get()

            res.x += self.box.rect.x
            res.y += self.box.rect.y

            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h

            return res

        self.fun = fun

        # this is probably the dirties code I've ever written in my entire life
        def make_fun(size):
            ar = utils.get_aspect_ratio(Vector2(size))

            def fun(rect):
                res = rect.copy()
                pa = self.box.get()

                res.x += self.box.rect.x
                res.y += self.box.rect.y

                res.x *= pa.w
                res.y *= pa.h
                res.w *= pa.h / ar.y
                res.h *= pa.h

                return res

            return fun

        step_w = 1 / 3

        self.button_1_text = Texture.from_surface(
            cr.renderer, self.font.render("Folders", True, cr.color_theme.text_0)
        )
        self.button_2_text = Texture.from_surface(
            cr.renderer, self.font.render("Info", True, cr.color_theme.text_0)
        )
        self.button_3_text = Texture.from_surface(
            cr.renderer, self.font.render("Edit", True, cr.color_theme.text_0)
        )

        self.button_1_box = RelRect(
            make_fun(self.button_1_text.get_rect().size),
            step_w * 0,
            0,
            step_w,
            1,
            use_param=True,
        )
        self.button_2_box = RelRect(
            make_fun(self.button_2_text.get_rect().size),
            step_w * 1,
            0,
            step_w,
            1,
            use_param=True,
        )
        self.button_3_box = RelRect(
            make_fun(self.button_3_text.get_rect().size),
            step_w * 2,
            0,
            step_w,
            1,
            use_param=True,
        )

        self.box_list: list[RelRect] = [
            self.button_1_box,
            self.button_2_box,
            self.button_3_box,
        ]

        self.selected_box_index = SelectedInfoView.FOLDERS

    @property
    def selected_box(self) -> RelRect:
        return self.box_list[self.selected_box_index.value]

    def check_click(self):
        mr = cr.event_holder.mouse_rect
        click = cr.event_holder.mouse_pressed_keys[0]

        if click:
            for c, box, enum in zip(
                range(len(self.box_list)), self.box_list, SelectedInfoView_All
            ):
                rect = self.fun(box.rect)
                if mr.colliderect(rect):
                    self.selected_box_index = enum
                    cr.log.write_log(
                        f"Updated current info_view index to {c}", LogLevel.DEBUG
                    )
                    break

    def check_events(self):
        self.check_click()

    def render(self):
        self.selected_box.render(
            cr.color_theme.color_1,
            cr.color_theme.button,
            cr.color_theme.color_0,
            rect=self.fun(self.selected_box.rect),
        )

        s1 = self.button_1_box.get()
        s2 = self.button_2_box.get()
        s3 = self.button_3_box.get()

        r1 = self.fun(self.button_1_box.rect)
        s1.center = r1.center
        r2 = self.fun(self.button_2_box.rect)
        s2.center = r2.center
        r3 = self.fun(self.button_3_box.rect)
        s3.center = r3.center

        cut_1 = utils.cut_rect_in(r1, s1)
        cut_2 = utils.cut_rect_in(r2, s2)
        cut_3 = utils.cut_rect_in(r3, s3)

        src_rect_1 = utils.mult_rect(
            cut_1[1], self.button_1_text.width, self.button_1_text.height
        )
        src_rect_2 = utils.mult_rect(
            cut_2[1], self.button_2_text.width, self.button_2_text.height
        )
        src_rect_3 = utils.mult_rect(
            cut_3[1], self.button_3_text.width, self.button_3_text.height
        )

        # src_rect_1.center = self.button_1_box.get().center
        # cut_1[0].center = self.button_1_box.get().center

        self.button_1_text.draw(src_rect_1, cut_1[0])
        self.button_2_text.draw(src_rect_2, cut_2[0])
        self.button_3_text.draw(src_rect_3, cut_3[0])


# todo: find a better name for this class
