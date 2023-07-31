from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.hover_man import HoverMan
from gui.ui_layer import UiLayer
from helper_kit.relative_rect import RelRect
from core.common import utils, assets


# todo: properly center the bottom pane elements
class ImageUiLayer(UiLayer):
    def __init__(self, hover_man: HoverMan):
        super().__init__()
        self.hover_man = hover_man
        self.video_buttons = []
        self.picture_buttons = []
        self.play_button: Optional[Button] = None
        # a value between 0 and 1
        self.navigator_pos_scale = 0
        self.navigator_locked = False

    def init(self):
        self.init_right_pane()
        self.init_bottom_pane()

    def get_box(self):
        return self.parent.image_box

    @property
    def navigator_bar_height(self):
        pa = self.get_box().get()

        val = cr.ws().y * 0.01
        if val > pa.h * 0.1:
            val = pa.h * 0.1

        return val

    @property
    def navigator_button_width(self):
        bar = self.navigator_bar_rect

        val = cr.ws().y * 0.02
        if val > bar.w * 0.04:
            val = bar.w * 0.04

        return val

    @property
    def navigator_button_rect(self):
        bar = self.navigator_bar_rect
        return FRect(self.navigator_pos, bar.y, self.navigator_button_width, bar.h)

    @property
    def navigator_pos(self):
        bar = self.navigator_bar_rect
        bw = self.navigator_button_width

        return utils.lerp(bar.left, bar.right - bw, self.navigator_pos_scale / 1)

    @property
    def navigator_bar_rect(self):
        pa = self.get_box().get()
        bar = pa.copy()

        bar.h = self.navigator_bar_height
        bar.bottom = pa.bottom - pa.h * 0.025

        return bar

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
            "Play Video",
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
        self.picture_buttons.extend([next_button, previous_button])

    def trigger_fullscreen(self):
        if cr.gallery.get_current_view() == ViewType.FULLSCREEN:
            cr.gallery.update_current_view(ViewType.DETAILED)
        else:
            cr.gallery.update_current_view(ViewType.FULLSCREEN)

    def init_right_pane(self):
        def right_pane_render_condition():
            x = self.parent.image_box.get()
            mr = cr.event_holder.mouse_pos
            return mr.x > x.right - x.w * 0.05

        def source_function():
            x = self.parent.image_box.get()
            return x.x, x.y, x.w, x.w

        def delete_function():
            cr.clipboard.delete(cr.gallery.content_manager.current_content.path)

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
            self.trigger_fullscreen,
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

        def delete_render_condition():
            x = right_pane_render_condition()
            content = cr.gallery.content_manager.current_content
            return x and content not in assets.reserved_contents

        delete_button = Button(
            "Delete",
            R((0.95, h_step * 3), (0.05, 0.05)),
            assets.ui_buttons["delete"],
            delete_function,
            delete_render_condition,
        )

        self.buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, delete_button]
        )
        self.picture_buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, delete_button]
        )
        self.video_buttons.extend(
            [fullscreen_button, zoom_in_button, zoom_out_button, delete_button]
        )

    def update_navigator_button(self):
        content: Content = self.parent.content_manager.current_content
        total_time = content.video_total_time
        current_time = (
            content.opencv_video.get(cv2.CAP_PROP_POS_FRAMES) / content.video_fps
        )
        lerp_val = utils.inv_lerp(0, total_time, current_time)
        self.navigator_pos_scale = lerp_val

    def check_navigator(self):
        self.update_navigator_button()

        rect = self.navigator_bar_rect
        rect.w -= self.navigator_button_width

        pressed = cr.event_holder.mouse_pressed_keys[0]
        released = cr.event_holder.mouse_released_keys[0]
        held = cr.event_holder.mouse_held_keys[0]
        mr = cr.event_holder.mouse_rect
        mp = mr.center

        pa: FRect = self.get_box().get()

        # if not pa.contains(mr):
        #     self.navigator_locked = False
        #     return

        if pressed:
            if mr.colliderect(rect):
                self.navigator_locked = True

        if released:
            self.navigator_locked = False

        if self.navigator_locked:
            content: Content = self.parent.content_manager.current_content

            val = utils.inv_lerp(rect.left, rect.right, mp[0])

            if val < 0:
                val = 0
            if val > 1:
                val = 1

            self.navigator_pos_scale = val

            new_time = self.navigator_pos_scale * content.video_total_time
            if content.audio_extraction_result:
                content.video_music_start_time = new_time
                if pg.mixer_music.get_busy():
                    pg.mixer_music.stop()
                    pg.mixer_music.play(start=content.video_music_start_time)
                    content.sync_video_with_audio()
                else:
                    pg.mixer_music.stop()
                    pg.mixer_music.play(start=content.video_music_start_time)
                    pg.mixer_music.pause()
                    content.sync_video_with_audio()
            else:
                content.opencv_video.set(
                    cv2.CAP_PROP_POS_FRAMES, new_time * content.video_fps
                )

            content.update_frame()

    def check_hover_man(self):
        mr = cr.event_holder.mouse_rect

        for button in self.buttons:
            this = button.rel_rect.get()
            if mr.colliderect(this):
                self.hover_man.update_text(button.name)
                break

    # done: fix the bug in navigation
    def check_events(self):
        pa = self.get_box().get()
        mr = cr.event_holder.mouse_rect

        is_vid = False
        content = cr.gallery.content_manager.current_content
        if content.type in [ContentType.PICTURE, ContentType.GIF]:
            self.buttons = self.picture_buttons
        elif content.type == ContentType.VIDEO:
            self.buttons = self.video_buttons
            is_vid = True

        if is_vid:
            self.check_navigator()

        self.check_hover_man()
        super().check_events()
        if self.any_hovered:
            cr.mouse.current_cursor = pgl.SYSTEM_CURSOR_HAND
        else:
            if (
                cr.event_holder.mouse_double_clicked
                or pgl.K_RETURN in cr.event_holder.pressed_keys
            ) and pa.colliderect(mr):
                self.trigger_fullscreen()

    def render(self):
        is_vid = False
        content = cr.gallery.content_manager.current_content
        if content.type in [ContentType.PICTURE, ContentType.GIF]:
            self.buttons = self.picture_buttons
        elif content.type == ContentType.VIDEO:
            self.buttons = self.video_buttons
            is_vid = True

        super().render()

        if is_vid:
            cr.renderer.draw_color = cr.color_theme.color_2
            cr.renderer.fill_rect(self.navigator_bar_rect)

            cr.renderer.draw_color = cr.color_theme.navigator
            cr.renderer.fill_rect(self.navigator_button_rect)

            cr.renderer.draw_color = cr.color_theme.navigator_bar_border
            cr.renderer.draw_rect(self.navigator_bar_rect)
