from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.zoom_view import ZoomView
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


# done: add black formatter
class DetailedView:
    def __init__(self):
        self.last_ratio = utils.get_aspect_ratio(cr.ws())

        self.image_pos: Optional[Vector2] = Vector2(0.2, 0.1)
        self.image_size: Optional[Vector2] = Vector2(0.8, 0.65)

        self.top_box: Optional[RelRect] = None
        self.bottom_box: Optional[RelRect] = None
        self.detail_box: Optional[RelRect] = None

        self.image_box = RelRect(cr.ws, (0, 0), (0, 0))

        self.left_box: Optional[RelRect] = None
        self.info_box: Optional[RelRect] = None
        self.log_box: Optional[RelRect] = None
        self.preview_box: Optional[RelRect] = None

        """
        these fields are used to resize the image box & the relative rectangles group.
        whenever set to any value other than None, resize_boxes gets called and a new 
        size is set for the image_box, and so on the other rectangles.
        this operation resizes the relative rectangles based on image_box.
        """
        self.resize_x_request: Optional[float] = None
        self.resize_y_request: Optional[float] = None

        self.x_locked = False
        self.y_locked = False

        self.zoom_texture = random.choice(assets.pics)

        self.zoom_view = ZoomView(self.image_box, self.zoom_texture)

        self.resize_boxes()

    def resize_boxes(self):
        X, Y = cr.ws()
        rect = FRect(self.image_pos, self.image_size)

        if self.x_locked:
            x_val = utils.inv_lerp(0, X, self.resize_x_request)
            if x_val < 0.1:
                x_val = 0.1
            if x_val > 0.65:
                x_val = 0.65
            rect.x = x_val
            rect.w = abs(1 - rect.x)

        if self.y_locked:
            y_val = utils.inv_lerp(0, Y, self.resize_y_request)
            if y_val > 0.8:
                y_val = 0.8
            if y_val < 0.6:
                y_val = 0.6
            rect.h = abs(rect.y - y_val)

        image_pos = self.image_pos = Vector2(rect.x, rect.y)
        image_size = self.image_size = Vector2(rect.w, rect.h)

        self.top_box = RelRect(cr.ws, 0, 0, 1, 0.05)
        self.detail_box = RelRect(
            cr.ws, image_pos.x, self.top_box.rect.bottom, image_size.x, 0.05
        )
        self.bottom_box = RelRect(cr.ws, 0, 0.95, 1, 0.05)

        self.image_box.rect = FRect(self.image_pos, self.image_size)

        left_box_width = image_pos.x
        self.left_box = RelRect(cr.ws, 0, 0.1, left_box_width, image_size.y)

        self.info_box = RelRect(
            cr.ws,
            0,
            self.top_box.rect.y + self.top_box.rect.h,
            self.left_box.rect.w,
            0.05,
        )

        self.log_box = RelRect(
            cr.ws,
            0,
            self.left_box.rect.y + self.left_box.rect.h,
            self.left_box.rect.w,
            abs(self.left_box.rect.y + self.left_box.rect.h - self.bottom_box.rect.y),
        )

        self.preview_box = RelRect(
            cr.ws,
            image_pos.x,
            image_pos.y + image_size.y,
            image_size.x,
            abs(image_pos.y + image_size.y - self.bottom_box.rect.y),
        )

        self.zoom_view.update()

    def check_events(self):
        m_rect = cr.event_holder.mouse_rect
        held = cr.event_holder.mouse_held_keys[0]
        clicked = cr.event_holder.mouse_pressed_keys[0]

        if cr.event_holder.window_resized:
            self.resize_boxes()

        self.zoom_view.check_events()

        if pgl.K_SPACE in cr.event_holder.pressed_keys:
            self.zoom_view.image = random.choice(assets.pics)
            self.zoom_view.reset()
            self.zoom_view.update()

        if (
            m_rect.colliderect(self.image_box.get())
            and m_rect.colliderect(self.preview_box.get())
            and m_rect.colliderect(self.left_box.get())
        ):
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_SIZEALL

            if clicked:
                self.x_locked = True
                self.y_locked = True

        elif m_rect.colliderect(self.image_box.get()) and m_rect.colliderect(
            self.left_box.get()
        ):
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_SIZEWE
            if clicked:
                self.x_locked = True

        elif m_rect.colliderect(self.image_box.get()) and m_rect.colliderect(
            self.preview_box.get()
        ):
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_SIZENS
            if clicked:
                self.y_locked = True

        if cr.event_holder.mouse_released_keys[0]:
            self.x_locked = False
            self.y_locked = False
            self.resize_x_request = None
            self.resize_y_request = None

        if self.x_locked:
            self.resize_x_request = cr.event_holder.mouse_pos.x

        if self.y_locked:
            self.resize_y_request = cr.event_holder.mouse_pos.y

        if self.x_locked or self.y_locked:
            self.resize_boxes()

    def render_debug(self):
        ...

    def render(self):
        self.zoom_view.render()

        cr.renderer.draw_color = colors.CRIMSON
        cr.renderer.draw_rect(self.top_box.get())

        cr.renderer.draw_color = colors.CHOCOLATE
        cr.renderer.draw_rect(self.bottom_box.get())

        cr.renderer.draw_color = colors.FOREST_GREEN
        cr.renderer.draw_rect(self.log_box.get())

        cr.renderer.draw_color = colors.BROWN
        cr.renderer.draw_rect(self.info_box.get())

        cr.renderer.draw_color = colors.CORAL
        cr.renderer.draw_rect(self.detail_box.get())

        cr.renderer.draw_color = colors.DARK_SLATE_GRAY
        cr.renderer.draw_rect(self.preview_box.get())

        cr.renderer.draw_color = colors.BLUE
        cr.renderer.draw_rect(self.left_box.get())

        cr.renderer.draw_color = colors.NAVY
        cr.renderer.draw_rect(self.image_box.get())

        if cr.event_holder.should_render_debug:
            self.render_debug()


# todo: find the purpose of DetailedView.log_box box & choose a better name
