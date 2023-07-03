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
            "enter fullscreen",
            R((0.95, h_step * 0), (0.05, 0.05)),
            assets.ui_buttons["fullscreen_enter"],
        )

        zoom_in_button = Button(
            "zoom-in",
            R((0.95, h_step * 1), (0.05, 0.05)),
            assets.ui_buttons["zoom_in"],
            zoom_function(True),
        )

        zoom_out_button = Button(
            "zoom-out",
            R((0.95, h_step * 2), (0.05, 0.05)),
            assets.ui_buttons["zoom_out"],
            zoom_function(False),
        )

        reset_button = Button(
            "reset",
            R((0.95, h_step * 3), (0.05, 0.05)),
            assets.ui_buttons["reset"],
            reset_function,
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
