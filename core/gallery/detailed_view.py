from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content_manager import ContentManager
from gui.image_ui_layer import ImageUiLayer
from gui.thumbnail_view import ThumbnailView
from gui.zoom_view import ZoomView
from helper_kit.relative_rect import RelRect
from core.common import utils, assets
from gui.button import Button


# todo: precisely position the boxes so there is no vacant space between them
# done: add black formatter
class DetailedView:
    def __init__(self, content_manager: ContentManager):
        self.last_ratio = utils.get_aspect_ratio(cr.ws())
        self.content_manager = content_manager
        self.image_ui_layer = ImageUiLayer()

        self.image_pos: Optional[Vector2] = Vector2(0.2, 0.05)
        self.image_size: Optional[Vector2] = Vector2(0.8, 0.65)

        self.bottom_box: Optional[RelRect] = None
        self.detail_box: Optional[RelRect] = None

        self.image_box = RelRect(cr.ws, (0, 0), (0, 0))

        self.left_box: Optional[RelRect] = None
        self.info_box: Optional[RelRect] = None
        self.log_box: Optional[RelRect] = None
        self.preview_box: Optional[RelRect] = RelRect(cr.ws, (0, 0), (0, 0))

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
        self.thumbnail_view = ThumbnailView(self.preview_box, self.content_manager)
        self.zoom_view = ZoomView(self.image_box, self.content_manager)
        self.just_resized_boxes = False
        self.resize_boxes()

    def init(self):
        self.image_ui_layer.init()

    def resize_boxes(self):
        X, Y = cr.ws()
        rect = FRect(self.image_pos, self.image_size)
        self.just_resized_boxes = True
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

        self.detail_box = RelRect(cr.ws, image_pos.x, 0, image_size.x, 0.05)
        self.bottom_box = RelRect(cr.ws, 0, 0.95, 1, 0.05)

        self.image_box.rect = FRect(self.image_pos, self.image_size)

        left_box_width = image_pos.x
        self.left_box = RelRect(cr.ws, 0, 0.05, left_box_width, image_size.y)

        self.info_box = RelRect(
            cr.ws,
            0,
            0,
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

        self.preview_box.rect = FRect(
            image_pos.x,
            image_pos.y + image_size.y,
            image_size.x,
            abs(image_pos.y + image_size.y - self.bottom_box.rect.y),
        )

    def check_mouse_events(self):
        m_rect = cr.event_holder.mouse_rect
        clicked = cr.event_holder.mouse_pressed_keys[0]

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

    def check_events(self):
        self.just_resized_boxes = False

        if cr.event_holder.window_resized:
            self.resize_boxes()

        self.image_ui_layer.check_events()

        if pgl.K_r in cr.event_holder.pressed_keys or self.content_manager.was_updated:
            self.zoom_view.reset()

        self.zoom_view.update()
        if not self.image_ui_layer.any_hovered:
            self.zoom_view.check_events()
            self.check_mouse_events()
        else:
            self.zoom_view.is_grabbing = False

        if self.x_locked or self.y_locked:
            self.resize_boxes()

        self.thumbnail_view.check_events()

    def render_debug(self):
        ...

    def render(self):
        self.image_box.render(colors.GIMP_1, colors.GIMP_2)
        self.zoom_view.render()

        self.detail_box.render(colors.GIMP_1, colors.GIMP_2)
        self.log_box.render(colors.GIMP_1, colors.GIMP_2, colors.GIMP_0)
        self.preview_box.render(colors.GIMP_1, colors.GIMP_2)

        self.info_box.render(colors.GIMP_1, colors.GIMP_2, colors.GIMP_0)
        self.left_box.render(colors.GIMP_1, colors.GIMP_2, colors.GIMP_0)

        self.bottom_box.render(colors.GIMP_1, colors.GIMP_2)

        self.image_ui_layer.render()
        self.thumbnail_view.render()

        if cr.event_holder.should_render_debug:
            self.render_debug()


# todo: find the purpose of DetailedView.log_box box & choose a better name
