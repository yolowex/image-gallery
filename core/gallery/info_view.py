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
                res.w *= (pa.h / ar.y)
                res.h *= pa.h

                return res

            return fun

        step_w = 1 / 3

        self.button_1_text = Texture.from_surface(
            cr.renderer, self.font.render("Folders", True, colors.WHITE)
        )
        self.button_2_text = Texture.from_surface(
            cr.renderer, self.font.render("Info", True, colors.WHITE)
        )
        self.button_3_text = Texture.from_surface(
            cr.renderer, self.font.render("Edit", True, colors.WHITE)
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

        self.box_list: list[RelRect] = [self.button_1_box,self.button_2_box,self.button_3_box]
        self.selected_box_index = 1


    @property
    def selected_box(self) -> RelRect:
        return self.box_list[self.selected_box_index]


    def check_click(self):
        mr = cr.event_holder.mouse_rect
        click = cr.event_holder.mouse_pressed_keys[0]

        if click:
            for c,box in enumerate(self.box_list):
                rect = self.fun(box.rect)
                if mr.colliderect(rect):
                    self.selected_box_index = c
                    cr.log.write_log(f"Updated current info_view index to {c}",LogLevel.DEBUG)
                    break


    def check_events(self):
        self.check_click()

    def render(self):

        self.selected_box.render(colors.GIMP_1,colors.NEON,
            colors.GIMP_0,rect=self.fun(self.selected_box.rect))


        self.button_1_text.draw(None, self.button_1_box.get())
        self.button_2_text.draw(None, self.button_2_box.get())
        self.button_3_text.draw(None, self.button_3_box.get())





# todo: find a better name for this class
