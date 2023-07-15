from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.disk_cursor import DiskCursor
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from gui.hover_man import HoverMan
from gui.thumbnail_view import ThumbnailView
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


f = FileType


def iterate_on_flattened(dict_, function, depth=0):
    if "name" in dict_.keys():
        function(dict_, depth)
        depth += 1

    for i in dict_:
        item = dict_[i]
        if isinstance(item, dict):
            iterate_on_flattened(item, function, depth)


class FolderView:
    def __init__(
        self,
        box: RelRect,
        content_manager: ContentManager,
        hover_man: HoverMan,
        thumbnail_view: ThumbnailView,
    ):
        self.box = box
        self.content_manager = content_manager
        self.hover_man = hover_man
        self.thumbnail_view = thumbnail_view
        self.font = assets.fonts["mid"]

        self.text_box_list: list[tuple[Texture, RelRect, dict]] = []

        self.item_height = 0.035
        self.items_height_margin = 0.005
        self.indent_w = 0.05
        self.content_height = 0
        self.content_width = 0
        self.scroll_x_value = 0.0
        self.scroll_y_value = 0.0
        self.scroll_x_locked = False
        self.scroll_y_locked = False
        self.text_max_length = 20
        self.selected_item: Optional[tuple[RelRect, dict]] = None
        self.disk_cursor = DiskCursor()

        self.unloaded_folders_color = colors.WHITE.lerp(colors.BLACK, 0.2)
        self.loaded_folders_color = colors.WHITE.lerp(colors.BLACK, 0.0)

        self.error_color = colors.RED.lerp(colors.BLUE, 0.25)
        self.selection_box_color = colors.OLIVE

    def init(self):
        self.disk_cursor.init()
        self.sync_texts()

    @property
    def __horizontal_scroll_bar_height(self):
        return self.__vertical_scroll_bar_width

    @property
    def __horizontal_scroll_bar_rect(self):
        pa = self.box.get()
        h = self.__horizontal_scroll_bar_height
        w = pa.w * 0.99
        y = pa.y + pa.h - h
        x = pa.left

        return FRect(x, y, w, h)

    # done: fix the position of the horizontal scroll button rect
    @property
    def __horizontal_scroll_button_rect(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        bar_rect = self.__horizontal_scroll_bar_rect

        right_bound = self.content_width

        w = self.box.rect.w / self.content_width * pa.w

        if w > pa.w:
            w = pa.w

        lerp_value = utils.inv_lerp(0, abs(right_bound), abs(self.scroll_x_value))

        rect = FRect(
            utils.lerp(bar_rect.left, bar_rect.right, lerp_value),
            bar_rect.y,
            w,
            bar_rect.h,
        )

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

        lerp_value = utils.inv_lerp(0, abs(bottom_bound), abs(self.scroll_y_value))

        rect = FRect(
            bar_rect.x,
            utils.lerp(bar_rect.top, bar_rect.bottom - h, lerp_value),
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

    def __make_text(self, file_item: dict, depth) -> bool:
        if file_item["is_loaded"]:
            color = self.loaded_folders_color
        else:
            color = self.unloaded_folders_color

        if file_item["error"]:
            color = self.error_color

        le = len(self.text_box_list)
        text = file_item["name"]

        if len(text) >= self.text_max_length:
            text = text[: self.text_max_length - 3] + "..."

        is_loaded = file_item["is_loaded"]
        if is_loaded:
            text = "< " + text
        else:
            text = "> " + text

        surface = self.font.render(text, True, color)
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

        self.text_box_list.append((texture, box, file_item))
        return True

    def sync_texts(self):
        self.content_height = 0
        self.content_width = 0
        di = self.disk_cursor.contents_dict
        self.text_box_list.clear()
        iterate_on_flattened(di, self.__make_text)

    def check_scroll(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = Vector2(mr.center)
        mod = pgl.K_LCTRL in cr.event_holder.held_keys
        clicked = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]

        if not pa.contains(mr):
            return

        if mr.colliderect(pa):
            if mw:
                if mod:
                    self.scroll_x_value += mw * 0.025

                    if self.scroll_x_value > 0:
                        self.scroll_x_value = 0

                    right_bound = -self.content_width + (self.box.rect.h / ar.y)
                    if self.scroll_x_value < right_bound:
                        self.scroll_x_value = right_bound

                else:
                    self.scroll_y_value += mw * 0.04

                    if self.scroll_y_value > 0:
                        self.scroll_y_value = 0

                    bottom_bound = -self.content_height + 0.95
                    if self.scroll_y_value < bottom_bound:
                        self.scroll_y_value = bottom_bound

        if clicked:
            v_bar = self.__vertical_scroll_bar_rect
            h_bar = self.__horizontal_scroll_bar_rect

            if mr.colliderect(v_bar):
                self.scroll_x_locked = True

            if mr.colliderect(h_bar):
                self.scroll_y_locked = True

        if released:
            self.scroll_x_locked = False
            self.scroll_y_locked = False

        if self.scroll_x_locked:
            bar = self.__vertical_scroll_bar_rect
            bottom_bound = -self.content_height + 0.95
            val = utils.inv_lerp(bar.top, bar.bottom, mp.y)
            self.scroll_y_value = utils.lerp(0, bottom_bound, val)
            if self.scroll_y_value > 0:
                self.scroll_y_value = 0
            if self.scroll_y_value < bottom_bound:
                self.scroll_y_value = bottom_bound

        if self.scroll_y_locked:
            bar = self.__horizontal_scroll_bar_rect
            right_bound = self.content_width

            val = utils.inv_lerp(bar.left, bar.right, mp.x)
            self.scroll_x_value = -utils.lerp(0, right_bound, val)

            if self.scroll_x_value > 0:
                self.scroll_x_value = 0

            right_bound = -self.content_width + (self.box.rect.h / ar.y)
            if self.scroll_x_value < right_bound:
                self.scroll_x_value = right_bound

        if self.content_width < 1 / ar.y:
            self.scroll_x_value = 0

        if self.content_height < 1:
            self.scroll_y_value = 0

    def check_click(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = Vector2(mr.center)
        mod = pgl.K_LCTRL in cr.event_holder.held_keys
        clicked = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]

        if not pa.contains(mr):
            return

        if clicked:
            for _, box, item in self.text_box_list:
                this = box.get()

                if this.top > pa.bottom:
                    continue

                if this.bottom < pa.top:
                    continue

                if this.left > pa.right:
                    continue

                if this.right < pa.left:
                    continue

                if mr.colliderect(this):
                    self.selected_item = (box, item)

                    self.content_manager.reinit(item["path"])
                    self.thumbnail_view.reinit()

                    if not item["is_loaded"]:
                        self.disk_cursor.expand_folder_at(item["address"])
                        self.sync_texts()
                    else:
                        self.disk_cursor.collapse_folder_at(item["address"])
                        self.sync_texts()

    def check_hover(self):
        pa = self.box.get()
        ar = utils.get_aspect_ratio(self.box.rect.size)
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = Vector2(mr.center)
        mod = pgl.K_LCTRL in cr.event_holder.held_keys
        clicked = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]

        if not pa.contains(mr):
            return

        if not cr.event_holder.mouse_moved:
            for _, box, item in self.text_box_list:
                this = box.get()

                if this.top > pa.bottom:
                    continue

                if this.bottom < pa.top:
                    continue

                if this.left > pa.right:
                    continue

                if this.right < pa.left:
                    continue

                if mr.colliderect(this):
                    self.hover_man.update_text(item["name"])

    def check_events(self):
        self.check_hover()
        self.check_click()
        self.check_scroll()

    def render(self):
        pa = self.box.get()

        for text, box, _ in self.text_box_list:
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

        if self.selected_item is not None:
            box, item = self.selected_item
            rect = box.get()
            cr.renderer.draw_color = self.selection_box_color
            if pa.colliderect(rect):
                cut = utils.cut_rect_in(pa, rect)
                cr.renderer.draw_rect(cut[0])
