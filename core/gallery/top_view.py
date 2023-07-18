from core.common.themes import ColorThemes
from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from gui.button import Button
from gui.hover_man import HoverMan
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class TopView:
    def __init__(
        self, box: RelRect, content_manager: ContentManager, hover_man: HoverMan
    ):
        self.box = box
        self.hover_man = hover_man
        self.content_manager = content_manager
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

        self.ctime_text: Optional[Texture] = None
        self.size_text: Optional[Texture] = None
        self.resolution_text: Optional[Texture] = None
        self.name_text: Optional[Texture] = None

        self.name_tag_box: Optional[RelRect] = None
        self.resolution_tag_box: Optional[RelRect] = None
        self.size_tag_box: Optional[RelRect] = None
        self.ctime_tag_box: Optional[RelRect] = None

        self.sync_texts()

    def get_text_info(self, text: Texture, box: RelRect):
        r1 = self.fun(box.rect)
        s1 = box.get()
        cut_1 = utils.cut_rect_in(r1, s1)
        src_rect_1 = utils.mult_rect(cut_1[1], text.width, text.height)
        return cut_1[0], src_rect_1

    def sync_texts(self):
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

        self.name_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{self.content_manager.current_content.short_name}",
                True,
                cr.color_theme.text_0,
            ),
        )

        self.resolution_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{self.content_manager.current_content.resolution}",
                True,
                cr.color_theme.text_0,
            ),
        )

        self.size_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{self.content_manager.current_content.size}",
                True,
                cr.color_theme.text_0,
            ),
        )

        self.ctime_text = Texture.from_surface(
            cr.renderer,
            self.font.render(
                f"{self.content_manager.current_content.ctime}",
                True,
                cr.color_theme.text_0,
            ),
        )

        def make_box_fun(text: Texture, box: RelRect):
            main_fun = make_fun(text.get_rect().size)

            def fun(rect):
                container = self.fun(box.rect)
                this = main_fun(rect)
                this.center = container.center

                return this

            return fun

        left = 0.05
        step_w = (1 - left) / 4
        h = 0.6
        self.name_tag_box = RelRect(
            None,
            left + step_w * 0,
            (1 - h) / 2,
            step_w,
            h,
            use_param=True,
        )

        self.name_tag_box.scale_source_function = make_box_fun(
            self.name_text, self.name_tag_box
        )

        self.resolution_tag_box = RelRect(
            None,
            left + step_w * 1,
            (1 - h) / 2,
            step_w,
            h,
            use_param=True,
        )

        self.resolution_tag_box.scale_source_function = make_box_fun(
            self.resolution_text, self.resolution_tag_box
        )

        self.size_tag_box = RelRect(
            None,
            left + step_w * 2,
            (1 - h) / 2,
            step_w,
            h,
            use_param=True,
        )

        self.size_tag_box.scale_source_function = make_box_fun(
            self.size_text, self.size_tag_box
        )

        self.ctime_tag_box = RelRect(
            None,
            left + step_w * 3,
            (1 - h) / 2,
            step_w,
            h,
            use_param=True,
        )

        self.ctime_tag_box.scale_source_function = make_box_fun(
            self.ctime_text, self.ctime_tag_box
        )

    def check_click(self):
        click = cr.event_holder.mouse_pressed_keys[0]
        mr = cr.event_holder.mouse_rect

    def check_hover(self):
        mr = cr.event_holder.mouse_rect

        name_info = self.get_text_info(self.name_text, self.name_tag_box)
        resolution_info = self.get_text_info(
            self.resolution_text, self.resolution_tag_box
        )
        ctime_info = self.get_text_info(self.ctime_text, self.ctime_tag_box)
        size_info = self.get_text_info(self.size_text, self.size_tag_box)

        if mr.colliderect(name_info[0]):
            self.hover_man.update_text(self.content_manager.current_content.name)

    def check_events(self):
        self.check_click()
        self.check_hover()

    def render(self):
        pa = self.box.get()
        # cr.renderer.draw_color = colors.RED
        # cr.renderer.draw_rect(pa)

        cr.renderer.draw_color = cr.color_theme.color_2
        cr.renderer.draw_rect(self.get_border_rect(self.name_tag_box))
        cr.renderer.draw_rect(self.get_border_rect(self.resolution_tag_box))
        cr.renderer.draw_rect(self.get_border_rect(self.size_tag_box))
        cr.renderer.draw_rect(self.get_border_rect(self.ctime_tag_box))

        name_info = self.get_text_info(self.name_text, self.name_tag_box)
        resolution_info = self.get_text_info(
            self.resolution_text, self.resolution_tag_box
        )
        ctime_info = self.get_text_info(self.ctime_text, self.ctime_tag_box)
        size_info = self.get_text_info(self.size_text, self.size_tag_box)

        self.name_text.draw(name_info[1], name_info[0])
        self.resolution_text.draw(resolution_info[1], resolution_info[0])
        self.ctime_text.draw(ctime_info[1], ctime_info[0])
        self.size_text.draw(size_info[1], size_info[0])

    def get_border_rect(self, box: RelRect):
        real = self.fun(box.rect)
        lc = real.center
        real.h = self.box.get().h
        real.center = lc
        return real
