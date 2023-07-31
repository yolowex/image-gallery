from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.text_view import TextView
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

        self.button_1_text = Texture.from_surface(
            cr.renderer, self.font.render("Folders", True, cr.color_theme.text_0)
        )
        self.button_2_text = Texture.from_surface(
            cr.renderer, self.font.render("Tags", True, cr.color_theme.text_0)
        )
        self.button_3_text = Texture.from_surface(
            cr.renderer, self.font.render("Edit", True, cr.color_theme.text_0)
        )

        step_w = 1 / 3

        self.box_1 = RelRect(
            fun,
            step_w * 0,
            0,
            step_w,
            1,
            use_param=True,
        )

        self.box_2 = RelRect(
            fun,
            step_w * 1,
            0,
            step_w,
            1,
            use_param=True,
        )

        self.box_3 = RelRect(
            fun,
            step_w * 2,
            0,
            step_w,
            1,
            use_param=True,
        )

        self.text_view_1 = TextView(self.box_1, False, "Folders", y_scale=0.5)
        self.text_view_2 = TextView(self.box_2, False, "Tags", y_scale=0.5)
        self.text_view_3 = TextView(self.box_3, False, "Edit", y_scale=0.5)

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

    def update_texts(self):
        self.text_view_1.update()
        self.text_view_2.update()
        self.text_view_3.update()

    @property
    def selected_box(self) -> RelRect:
        return self.box_list[self.selected_box_index.value]

    def check_click(self):
        mr = cr.event_holder.mouse_rect
        click = cr.event_holder.mouse_pressed_keys[0]
        # unsafe: dirty
        content: Content = cr.gallery.content_manager.current_content

        if self.selected_box_index == SelectedInfoView.EDIT:
            if (
                content in assets.reserved_contents
                or content.type != ContentType.PICTURE
            ):
                self.selected_box_index = SelectedInfoView.FOLDERS

        if click:
            for c, box, enum in zip(
                range(len(self.box_list)), self.box_list, SelectedInfoView_All
            ):
                if c == 2:
                    if (
                        content in assets.reserved_contents
                        or content.type != ContentType.PICTURE
                    ):
                        continue

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
        self.text_view_1.render()
        self.text_view_2.render()
        self.text_view_3.render()

        rect = self.fun(self.selected_box.rect)
        cr.renderer.draw_color = cr.color_theme.button
        cr.renderer.draw_rect(rect)


# todo: find a better name for this class
