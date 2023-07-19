from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class ContextMenuInfo:
    def __init__(self):
        self.items: list[list] = []

    @property
    def ljust_value(self):
        return int(max([len(i) for i in self.texts]) * 1.5)

    @property
    def texts(self):
        return [i[0] for i in self.items]

    @property
    def functions(self):
        return [i[1] for i in self.items]

    def add_item(self, text: str, function):
        self.items.append([text, function])


class ContextMenu:
    __default_info = ContextMenuInfo()
    __default_info.add_item("Copy", lambda x: print(x))
    __default_info.add_item("Cut", lambda x: print(x))
    __default_info.add_item("Delete", lambda x: print(x))
    __default_info.add_item("Paste", lambda x: print(x))
    __default_info.add_item("Save", lambda x: print(x))

    def __init__(self):
        self.top_left: Optional[Vector2] = None
        self.padding_x = 0.025
        self.padding_y = 0.005
        self.is_open = False
        self.font = assets.fonts["small"]

        self.info: Optional[ContextMenuInfo] = None
        self.texture_list: list[Texture] = []

        self.container_rect: FRect = FRect(0,0,0,0)
        self.rect_list: list[FRect] = []



    def update_rect_info(self):
        if not self.is_open:
            return

        win_rect = cr.ws_rect()
        width_list = [i.width + win_rect.w * self.padding_x for i in self.texture_list]
        height_list = [i.height + win_rect.h * self.padding_y for i in self.texture_list]

        container_rect = FRect(self.top_left.x,self.top_left.y,max(width_list),sum(height_list))

        if container_rect.right > win_rect.right:
            container_rect.right = container_rect.left

        if container_rect.bottom > win_rect.bottom:
            container_rect.bottom = container_rect.top

        self.container_rect.update(container_rect)
        self.rect_list.clear()

        for c,i in enumerate(height_list):
            y = sum([0] + height_list[:c])

            rect = FRect(container_rect.topleft,(container_rect.width,i))
            rect.y += y
            self.rect_list.append(rect)


    def init_text(self, text:str) -> Texture:
        ws = cr.ws()
        self.top_left = cr.event_holder.mouse_pos.copy()


        text = text.ljust(self.info.ljust_value)

        surface = self.font.render(text, True, cr.color_theme.text_0)
        new_surface = Surface(
            (
                surface.get_width() + ws.x * self.padding_x,
                surface.get_height() + ws.y * self.padding_y,
            )
        )

        new_surface.fill(colors.GLASS)

        rect = surface.get_rect(center=new_surface.get_rect().center)
        new_surface.blit(surface, rect)

        texture = Texture.from_surface(cr.renderer, new_surface)
        return texture

    def sync_texts(self):
        self.texture_list.clear()

        for text in self.info.texts:
            self.texture_list.append(self.init_text(text))

        self.update_rect_info()


    def open_menu(self, context_menu_info: ContextMenuInfo = None):
        if context_menu_info is None:
            self.info = ContextMenu.__default_info
        else:
            self.info = context_menu_info

        self.is_open = True
        self.top_left = cr.event_holder.mouse_pos.copy()
        self.sync_texts()


    def close_menu(self):
        self.is_open = False

    def check_events(self):
        self.update_rect_info()
        left_clicked = cr.event_holder.mouse_pressed_keys[0]
        right_clicked = cr.event_holder.mouse_pressed_keys[2]
        mr = cr.event_holder.mouse_rect

        if cr.event_holder.window_resized:
            self.close_menu()

        if not self.is_open:
            if right_clicked:
                self.open_menu()

        else:
            if mr.colliderect(self.container_rect):
                ...
            else:
                if left_clicked or right_clicked:
                    self.close_menu()

    def render(self):
        if not self.is_open:
            return

        cr.renderer.draw_color = cr.color_theme.color_2
        cr.renderer.fill_rect(self.container_rect)

        cr.renderer.draw_color = cr.color_theme.color_0
        cr.renderer.draw_rect(self.container_rect)

        for texture,rect in list(zip(self.texture_list,self.rect_list)):
            cr.renderer.draw_color = cr.color_theme.navigator


            cr.renderer.draw_color = cr.color_theme.error
            cr.renderer.draw_rect(rect)

            texture.draw(None,rect)

