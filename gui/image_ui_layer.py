from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


class ImageUiLayer(UiLayer):
    def __init__(self):
        super().__init__()
        self.init_right_pane()
        self.init_bottom_pane()

    def init_bottom_pane(self):
        def bottom_pane_render_condition():
            x = cr.gallery.detailed_view.image_box.get()
            mr = cr.event_holder.mouse_pos
            return mr.x > x.right - x.w*0.05


        def source_function(rect:FRect):
            rect = rect.copy()

            x = cr.gallery.detailed_view.image_box.get()

            rect.w *= x.w
            rect.h *= x.w

            return rect


        R = lambda *x: RelRect(source_function, *x,use_param=True)

        w_step = 0.1

        play_button = Button(
            "Play",
            R((0.5+w_step*0,0.9), (0.05, 0.05)),
            assets.ui_buttons["play"],
        )


        self.buttons.extend(
            [play_button]
        )

    def init_right_pane(self):
        def right_pane_render_condition():
            x = cr.gallery.detailed_view.image_box.get()
            mr = cr.event_holder.mouse_pos
            return mr.x > x.right - x.w*0.05


        def source_function():
            x = cr.gallery.detailed_view.image_box.get()
            return x.x, x.y, x.w, x.w

        def reset_function():
            cr.gallery.detailed_view.zoom_view.reset()
            cr.gallery.detailed_view.zoom_view.check_events()

        def zoom_function(in_: bool):
            def do_zoom():
                current_zoom = cr.gallery.detailed_view.zoom_view.zoom
                if in_:
                    current_zoom += 0.25
                else:
                    current_zoom -= 0.25

                image_box = cr.gallery.detailed_view.image_box.get()

                cr.gallery.detailed_view.zoom_view.do_zoom(
                    current_zoom, Vector2(image_box.center)
                )

            return do_zoom

        R = lambda *x: RelRect(source_function, *x)

        h_step = 0.06

        enter_fs_button = Button(
            "Enter fullscreen",
            R((0.95, h_step * 0), (0.05, 0.05)),
            assets.ui_buttons["fullscreen_enter"],
        )

        zoom_in_button = Button(
            "Zoom-in",
            R((0.95, h_step * 1), (0.05, 0.05)),
            assets.ui_buttons["zoom_in"],
            zoom_function(True),
            right_pane_render_condition
        )

        zoom_out_button = Button(
            "Zoom-out",
            R((0.95, h_step * 2), (0.05, 0.05)),
            assets.ui_buttons["zoom_out"],
            zoom_function(False),
            right_pane_render_condition
        )

        reset_button = Button(
            "Reset",
            R((0.95, h_step * 3), (0.05, 0.05)),
            assets.ui_buttons["reset"],
            reset_function,
            right_pane_render_condition
        )

        self.buttons.extend(
            [enter_fs_button, zoom_in_button, zoom_out_button, reset_button]
        )

    def check_events(self):
        super().check_events()
        if self.any_hovered:
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_HAND

    def render(self):
        super().render()
