from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


f = FileType

test_dict = {}


def make_test_dict(dict_, depth=0):
    mx = 4
    d = depth + 1
    if depth >= mx:
        d = mx

    egg = 3

    if depth >= mx:
        return

    for i in range(egg):
        t = random.choice([f.FILE, f.DIR, f.DIR, f.DIR])
        t = t.DIR

        item = {"name": f"{t.name.lower()}-{i}-{depth}", "file_type": t}
        dict_[i] = item

        if item["file_type"] == f.DIR:
            make_test_dict(item, depth + 1)


make_test_dict(test_dict)


def iterate_on_flattened(dict_, function, depth=0):
    if "name" in dict_.keys():
        function(dict_, depth)
        depth += 1

    for i in dict_:
        item = dict_[i]
        if isinstance(item, dict):
            iterate_on_flattened(item, function, depth)


class FolderView:
    def __init__(self, box: RelRect, content_manager: ContentManager):
        self.box = box
        self.content_manager = content_manager
        self.font = assets.fonts["mid"]

        self.text_box_list: list[tuple[Texture, RelRect]] = []

        self.item_height = 0.025
        self.items_height_margin = 0.005
        self.indent_w = 0.1
        self.content_height = 0
        self.content_width = 0
        self.scroll_x_value = 0.0
        self.scroll_y_value = 0.0

        self.init_texts()


    @property
    def __horizontal_scroll_bar_height(self) :
        return self.__vertical_scroll_bar_width


    @property
    def __horizontal_scroll_bar_rect(self) :
        pa = self.box.get()
        h = self.__horizontal_scroll_bar_height
        w = pa.w * 0.99
        y = pa.y + pa.h - h
        x = pa.left

        return FRect(x, y, w, h)


    @property
    def __horizontal_scroll_button_rect(self) :
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        bar_rect = self.__horizontal_scroll_bar_rect

        right_bound = 1 / ar.y


        w = self.box.rect.w / self.content_width * pa.w

        if w > pa.w :
            w = pa.w

        lerp_value = utils.inv_lerp(0, abs(right_bound), abs(self.scroll_x_value))

        rect = FRect(
            utils.lerp(bar_rect.left, bar_rect.right - w, lerp_value),
            bar_rect.y,
            w,
            bar_rect.h )

        return rect

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
        h = pa.h - self.__horizontal_scroll_bar_rect.h

        return FRect(x, y, w, h)

    @property
    def __vertical_scroll_button_rect(self):
        pa = self.box.get()
        bar_rect = self.__vertical_scroll_bar_rect

        bottom_bound = -self.content_height + 0.95

        h = self.box.rect.h / self.content_height * pa.h

        if h > pa.h:
            h = pa.h


        lerp_value = utils.inv_lerp(0,abs(bottom_bound),abs(self.scroll_y_value))

        rect = FRect(
            bar_rect.x,
            utils.lerp(bar_rect.top,bar_rect.bottom-h,lerp_value),
            bar_rect.w,
            h,
        )

        return rect

    def __make_fun(self, size):
        ar = utils.get_aspect_ratio(Vector2(size))

        def fun(rect):
            res = rect.copy()
            pa = self.box.get()

            res.x += self.box.rect.x + self.scroll_x_value
            res.y += self.box.rect.y + self.scroll_y_value

            res.x *= pa.h
            res.y *= pa.h
            res.w *= pa.h / ar.y
            res.h *= pa.h

            res.x += self.__vertical_scroll_bar_width

            return res

        return fun

    def __make_text(self, file_item: dict, depth):
        le = len(self.text_box_list)
        text = file_item["name"]
        surface = self.font.render(text, True, colors.WHITE, colors.BLACK)
        ar = utils.get_aspect_ratio(Vector2(surface.get_size()))
        texture = Texture.from_surface(cr.renderer, surface)

        box = RelRect(
            self.__make_fun(texture.get_rect().size),
            self.indent_w * depth,
            (self.item_height + self.items_height_margin) * le,
            self.item_height,
            self.item_height,
            use_param=True,
        )

        big_h = abs(box.rect.bottom)
        big_w = abs(box.rect.left + (box.rect.w / ar.y))

        if big_h > self.content_height:
            self.content_height = big_h

        if big_w > self.content_width:
            self.content_width = big_w

        self.text_box_list.append((texture, box))

    def init_texts(self):
        di = test_dict
        self.text_box_list.clear()
        iterate_on_flattened(di, self.__make_text)



    def check_scroll(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mod = pgl.K_LCTRL in cr.event_holder.held_keys

        if mr.colliderect(pa) :
            if mw :
                if mod :
                    self.scroll_x_value += mw * 0.025

                    if self.scroll_x_value > 0 :
                        self.scroll_x_value = 0

                    right_bound = -self.content_width + (self.box.rect.h / ar.y)
                    if self.scroll_x_value < right_bound :
                        self.scroll_x_value = right_bound

                else :
                    self.scroll_y_value += mw * 0.04

                    if self.scroll_y_value > 0 :
                        self.scroll_y_value = 0

                    bottom_bound = -self.content_height + 0.95
                    if self.scroll_y_value < bottom_bound :
                        self.scroll_y_value = bottom_bound


        if self.content_width < 1/ar.y:
            self.scroll_x_value = 0

        if self.content_height < 1:
            self.scroll_y_value = 0


    def check_events(self):
        self.check_scroll()

    def render(self):
        pa = self.box.get()

        for text, box in self.text_box_list:
            this = box.get()

            if this.top > pa.bottom:
                continue

            if this.bottom < pa.top:
                continue

            if this.left > pa.right:
                continue

            if this.right < pa.left:
                continue

            cut = utils.cut_rect_in(pa, this)
            mult = utils.mult_rect(cut[1], text.width, text.height)

            text.draw(mult, cut[0])

        cr.renderer.draw_color = constants.colors.GIMP_1
        cr.renderer.fill_rect(self.__vertical_scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.BEIGE
        cr.renderer.draw_rect(self.__vertical_scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.NEON
        cr.renderer.fill_rect(self.__vertical_scroll_button_rect)

        cr.renderer.draw_color = constants.colors.GIMP_1
        cr.renderer.fill_rect(self.__horizontal_scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.BEIGE
        cr.renderer.draw_rect(self.__horizontal_scroll_bar_rect)

        cr.renderer.draw_color = constants.colors.NEON
        cr.renderer.fill_rect(self.__horizontal_scroll_button_rect)
