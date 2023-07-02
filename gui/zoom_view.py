from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils


class ZoomView:
    def __init__(self, container_box: RelRect, image: Texture):
        self.container_box = container_box
        self.image = image
        self.inner_image_rect = FRect(0, 0, 0, 0)
        self.zoom = 1
        self.is_grabbing = False
        self.grab_src = Vector2(0, 0)
        self.grab_dst = Vector2(0, 0)
        self.current_rel = Vector2(0, 0)

    def reset(self):
        self.zoom = 1
        self.is_grabbing = False
        self.grab_src = Vector2(0, 0)
        self.grab_dst = Vector2(0, 0)
        self.current_rel = Vector2(0, 0)

    def update(self):
        self.inner_image_rect = self.container_box.get_in_rect(
            Vector2(self.image.get_rect().size), window_relative=True
        )


    @property
    def x_grab_allowed(self) -> bool:
        """
        this function determines if the user is allowed to
        grab the picture and move it towards the x-axis.
        :return:
        """

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom

        return n_rect.w > self.container_box.get().w


    @property
    def y_grab_allowed(self) -> bool :
        """
        this function determines if the user is allowed to
        grab the picture and move it towards the y-axis.
        :return:
        """

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom

        return n_rect.h > self.container_box.get().h


    def get_picture_rect(self):
        grab_diff = self.grab_dst - self.grab_src
        l_rect = self.inner_image_rect.copy()

        if self.x_grab_allowed :
            l_rect.x += grab_diff.x + self.current_rel.x
        else:
            self.current_rel.x = 0

        if self.y_grab_allowed :
            l_rect.y += grab_diff.y + self.current_rel.y
        else:
            self.current_rel.y= 0

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom
        n_rect.center = l_rect.center

        return n_rect


    def check_events(self):
        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mod = pgl.K_LCTRL in cr.event_holder.held_keys
        if mw != 0 and mod:
            self.zoom *= 1 + mw * 0.04


        if mr.colliderect(self.get_picture_rect()) and mr.colliderect(self.container_box.get()):
            if cr.event_holder.mouse_pressed_keys[0]:
                self.is_grabbing = True
                self.grab_src = cr.event_holder.mouse_pos.copy()
                self.grab_dst = cr.event_holder.mouse_pos.copy()

            if cr.event_holder.mouse_moved and self.is_grabbing:
                self.grab_dst = cr.event_holder.mouse_pos.copy()

            if cr.event_holder.mouse_released_keys[0]:
                self.is_grabbing = False
                grab_diff = self.grab_dst - self.grab_src
                self.current_rel += grab_diff

                self.grab_src = Vector2(0, 0)
                self.grab_dst = Vector2(0, 0)

            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_HAND

        else:
            self.is_grabbing = False
            grab_diff = self.grab_dst - self.grab_src
            self.current_rel += grab_diff

            self.grab_src = Vector2(0, 0)
            self.grab_dst = Vector2(0, 0)

        if mr.colliderect(self.container_box.get()) and mod:
            cr.mouse.current_cursor = pg.cursors.broken_x

    def render_debug(self):
        ...

    def render(self):
        # dst_rect = self.container_box.cut_rect_in(self.inner_image_rect)
        # todo: cut the picture in case it is bigger than the box size

        self.image.draw(None, self.get_picture_rect())

        if cr.event_holder.should_render_debug:
            self.render_debug()
