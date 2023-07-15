from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.button import Button
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


# todo: properly center the bottom pane elements
class ImageUiLayer(UiLayer):
    def __init__(self):
        super().__init__()
        self.video_buttons = []
        self.picture_buttons = []
        self.play_button: Optional[Button] = None

    def init(self):
        self.init_right_pane()
        self.init_bottom_pane()

    @property
    def parent(self):
        if cr.gallery.get_current_view() == ViewType.DETAILED:
            return cr.gallery.detailed_view

        return cr.gallery.fullscreen_view

    def reset_trigger_button(self):
        self.play_button.image = assets.ui_buttons["play"]

    def reverse_trigger_button(self):
        content = cr.gallery.content_manager.current_content

        if content.video_is_paused or not content.video_is_started:
            self.play_button.image = assets.ui_buttons["play"]
        else:
            self.play_button.image = assets.ui_buttons["pause"]

    def trigger_start(self):
        cr.gallery.content_manager.trigger_media()
        self.reverse_trigger_button()

    def init_bottom_pane(self):
        def bottom_pane_render_condition():
            x = self.parent.image_box.get()
            mr = cr.event_holder.mouse_pos
            return mr.y > x.bottom - x.h * 0.2

        def source_function(rect: FRect):
            rect = rect.copy()

            x = self.parent.image_box.get()

            rect.x *= x.w
            rect.y *= x.h
            rect.x += x.x
            rect.y += x.y
            rect.w *= x.h
            rect.h *= x.h

            return rect

        R = lambda *x: RelRect(source_function, *x, use_param=True)

        play_button_size = (0.1, 0.1)
        other_buttons_size = (0.08, 0.08)
        play_button_y = 0.85
        other_buttons_y = (
            play_button_y + (play_button_size[0] - other_buttons_size[0]) / 2
        )

        w_step = play_button_size[0]

        self.play_button = Button(
            "Play",
            R((0.46 + w_step * 0, play_button_y), play_button_size),
            assets.ui_buttons["play"],
            self.trigger_start,
            bottom_pane_render_condition,
        )

        next_button = Button(
            "Next",
            R((0.46 + w_step * 1, other_buttons_y), other_buttons_size),
            assets.ui_buttons["play_go_next"],
            cr.gallery.content_manager.go_next,
            bottom_pane_render_condition,
        )

        previous_button = Button(
            "Previous",
            R((0.46 + w_step * -1, other_buttons_y), other_buttons_size),
            assets.ui_buttons["play_go_previous"],
            cr.gallery.content_manager.go_previous,
            bottom_pane_render_condition,
        )

        back_button = Button(
            "Back",
            R((0.46 + w_step * -2, other_buttons_y), other_buttons_size),
            assets.ui_buttons["play_go_first"],
            cr.gallery.content_manager.go_back,
            bottom_pane_render_condition,
        )
        forward_button = Button(
            "Forward",
            R((0.46 + w_step * 2, other_buttons_y), other_buttons_size),
            assets.ui_buttons["play_go_last"],
            cr.gallery.content_manager.go_forward,
            bottom_pane_render_condition,
        )

        self.buttons.extend([])

        self.video_buttons.extend(
            [
                self.play_button,
                next_button,
                previous_button,
                back_button,
                forward_button,
            ]
        )
        print(len(self.video_buttons))
        self.picture_buttons.extend([next_button, previous_button])

    def init_right_pane(self):
        def right_pane_render_condition():
            x = self.parent.image_box.get()
            mr = cr.event_holder.mouse_pos
            return mr.x > x.right - x.w * 0.05

        def source_function():
            x = self.parent.image_box.get()
            return x.x, x.y, x.w, x.w

        def fullscreen_function():
            if cr.gallery.get_current_view() == ViewType.FULLSCREEN:
                cr.gallery.update_current_view(ViewType.DETAILED)
            else:
                cr.gallery.update_current_view(ViewType.FULLSCREEN)

        def reset_function():
            self.parent.zoom_view.reset()
            self.parent.zoom_view.check_events()

        def zoom_function(in_: bool):
            def do_zoom():
                text = "in"
                current_zoom = self.parent.zoom_view.zoom
                if in_:
                    current_zoom += 0.25
                else:
                    text = "out"
                    current_zoom -= 0.25

                image_box = self.parent.image_box.get()
                """
                adding these two lines fixed bug#1 and bug#2.
                this is probably a bad solution.
                """
                self.parent.zoom_view.check_events()
                self.parent.zoom_view.do_zoom(current_zoom, Vector2(image_box.center))

            return do_zoom

        R = lambda *x: RelRect(source_function, *x)

        h_step = 0.06

        fullscreen_button = Button(
            "Trigger fullscreen",
            R((0.95, h_step * 0), (0.05, 0.05)),
            assets.ui_buttons["fullscreen_enter"],
            fullscreen_function,
            right_pane_render_condition,
        )

        zoom_in_button = Button(
            "Zoom-in",
            R((0.95, h_step * 1), (0.05, 0.05)),
            assets.ui_buttons["zoom_in"],
            zoom_function(True),
            right_pane_render_condition,
        )

        zoom_out_button = Button(
            "Zoom-out",
            R((0.95, h_step * 2), (0.05, 0.05)),
            assets.ui_buttons["zoom_out"],
            zoom_function(False),
            right_pane_render_condition,
        )

        reset_button = Button(
            "Reset",
            R((0.95, h_step * 3), (0.05, 0.05)),
            assets.ui_buttons["reset"],
            reset_function,
            right_pane_render_condition,
        )

        self.buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, reset_button]
        )
        self.picture_buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, reset_button]
        )
        self.video_buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, reset_button]
        )

    # todo: fix the bug in navigation
    def check_events(self):
        content = cr.gallery.content_manager.current_content
        if content.type in [ContentType.PICTURE, ContentType.GIF]:
            self.buttons = self.picture_buttons
        elif content.type == ContentType.VIDEO:
            self.buttons = self.video_buttons

        super().check_events()
        if self.any_hovered:
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_HAND

    def render(self):
        super().render()
