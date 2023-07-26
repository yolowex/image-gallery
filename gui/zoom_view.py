from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from core.gallery.content_manager import ContentManager
from helper_kit.relative_rect import RelRect
from core.common import utils


class ZoomView:
    def __init__(self, container_box: RelRect, content_manager: ContentManager):
        self.content_manager = content_manager

        self.container_box = container_box

        self.inner_image_rect = FRect(0, 0, 0, 0)
        self.zoom = 1
        self.zoom_power = 0.1
        self.zoom_pos = Vector2(0, 0)

        self.is_grabbing = False
        self.grab_src = Vector2(0, 0)
        self.grab_dst = Vector2(0, 0)
        self.current_rel = Vector2(0, 0)
        self.__picture_rect = FRect(0, 0, 0, 0)

    @property
    def content(self):
        return self.content_manager.current_content

    def sync(self, target):
        target.zoom = self.zoom
        target.current_rel = self.current_rel.copy()
        target.is_grabbing = False

    def reset(self):
        self.zoom = 1
        self.is_grabbing = False
        self.grab_src = Vector2(0, 0)
        self.grab_dst = Vector2(0, 0)
        self.current_rel = Vector2(0, 0)

    def update(self):
        self.inner_image_rect = self.container_box.get_in_rect(
            Vector2(self.content.texture.get_rect().size), window_relative=True
        )

        self.update_picture_rect()

    @property
    def x_grab_allowed(self) -> bool:
        """
        this function determines if the user is allowed to
        grab the picture and move it towards the x-axis.
        :return: boolean
        """

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom

        return n_rect.w > self.container_box.get().w

    @property
    def y_grab_allowed(self) -> bool:
        """
        this function determines if the user is allowed to
        grab the picture and move it towards the y-axis.
        :return: boolean
        """

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom

        return n_rect.h > self.container_box.get().h

    def update_picture_rect(self):
        """
        this function returns the rectangle of the picture that is currently
        being shown, regarding the zoom, and current_rel/grab values.
        this function updates self.__picture_rect.
        :return: None
        """
        grab_diff = self.grab_dst - self.grab_src
        l_rect = self.inner_image_rect.copy()

        con_rect = self.container_box.get()

        if self.x_grab_allowed:
            l_rect.x += grab_diff.x + self.current_rel.x
        else:
            self.current_rel.x = 0

        if self.y_grab_allowed:
            l_rect.y += grab_diff.y + self.current_rel.y
        else:
            self.current_rel.y = 0

        n_rect = self.inner_image_rect.copy()
        n_rect.w *= self.zoom
        n_rect.h *= self.zoom
        n_rect.center = l_rect.center

        # todo: prohibit invalid current_rel movements
        if self.x_grab_allowed:
            if n_rect.left > con_rect.left:
                n_rect.left = con_rect.left

            if n_rect.right < con_rect.right:
                n_rect.right = con_rect.right

        if self.y_grab_allowed:
            if n_rect.bottom < con_rect.bottom:
                n_rect.bottom = con_rect.bottom

            if n_rect.top > con_rect.top:
                n_rect.top = con_rect.top

        self.__picture_rect = n_rect

    def get_picture_rect(self) -> FRect:
        """
        this function returns a copy of
        __picture_rect which is continuously being
        updated by update_picture_rect.

        :return: FRect
        """
        return self.__picture_rect.copy()

    def do_zoom(self, new_zoom: float, pivot_point: Vector2, use_rel_point=False):
        last_pic_rect = self.__picture_rect.copy()

        if use_rel_point:
            last_pic_point_rel = pivot_point
        else:
            last_pic_point_rel = utils.get_rel_point_in_rect(pivot_point, last_pic_rect)

        self.zoom = new_zoom

        if self.zoom < 1:
            self.zoom = 1
            self.current_rel = Vector2(0, 0)
        if self.zoom > 20:
            self.zoom = 20

        self.update_picture_rect()

        rel_stack = utils.stack_pin(
            last_pic_rect,
            last_pic_point_rel,
            self.__picture_rect,
            last_pic_point_rel,
        )

        # print(last_pic_point_rel,rel_stack)
        self.current_rel += rel_stack

        self.update_picture_rect()

    @property
    def should_check(self):
        is_detailed = cr.gallery.get_current_view() == ViewType.DETAILED
        tag_view = cr.gallery.detailed_view.tag_view

        # print(is_detailed,tag_view.any_name_tag_selected,len(tag_view.name_tags))

        return is_detailed and not tag_view.any_name_tag_selected

    def check_events(self):
        if not self.should_check:
            return

        self.content.check_events()

        mw = cr.event_holder.mouse_wheel
        mr = cr.event_holder.mouse_rect
        mp = cr.event_holder.mouse_pos
        mod = pgl.K_LCTRL in cr.event_holder.held_keys

        # done: implement precise zooming feature
        if (
            mw != 0
            and mod
            and mr.colliderect(self.container_box.get())
            and mr.colliderect(self.get_picture_rect())
        ):
            zoom = self.zoom * (1 + mw * self.zoom_power)
            self.do_zoom(zoom, mp)

        if mr.colliderect(self.get_picture_rect()) and mr.colliderect(
            self.container_box.get()
        ):
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

        if (
            mr.colliderect(self.container_box.get())
            and mr.colliderect(self.get_picture_rect())
            and mod
        ):
            cr.mouse.current_cursor = pg.cursors.broken_x

        elif mr.colliderect(self.container_box.get()) and mod:
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_NO

    def render(self):
        # dst_rect = self.container_box.cut_rect_in(self.inner_image_rect)
        # canceled: cut the picture in case it is bigger than the box size

        self.content.render(self.get_picture_rect())
