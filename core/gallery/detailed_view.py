from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect

# todo: add black formatter
class DetailedView:
    def __init__(self):
        image_pos = Vector2(0.2,0.1)
        image_size = Vector2(0.8,0.65)

        self.top_box = RelRect(cr.ws,0,0,1,0.05)
        self.bottom_box = RelRect(cr.ws,0,0.95,1,0.05)

        self.detail_box = RelRect(cr.ws,image_pos.x,image_pos.y-0.05,image_size.x,0.05)
        self.image_box = RelRect(cr.ws,image_pos,image_size)

        self.left_box = RelRect(
            cr.ws,
            0,
            image_pos.y,
            image_pos.x,
            image_size.y
        )

        self.info_box = RelRect(
            cr.ws,
            0,
            self.top_box.rect.y+self.top_box.rect.h,
            image_pos.x,
            abs(self.top_box.rect.y+self.top_box.rect.h-image_pos.y)
        )

        self.log_box = RelRect(
            cr.ws,
            0,
            self.left_box.rect.y+self.left_box.rect.h,
            image_pos.x,
            abs(self.left_box.rect.y+self.left_box.rect.h-self.bottom_box.rect.y)
        )

        self.preview_box = RelRect(
            cr.ws,
            image_pos.x,
            image_pos.y+image_size.y,
            image_size.x,
            abs(image_pos.y+image_size.y-self.bottom_box.rect.y)
        )


    def check_events(self):
        m_rect = cr.event_holder.mouse_rect


        if m_rect.colliderect(self.image_box.get()) and \
                m_rect.colliderect(self.preview_box.get()) \
                    and m_rect.colliderect(self.left_box.get()):
            pg.mouse.set_cursor(pgl.SYSTEM_CURSOR_SIZEALL)

        elif m_rect.colliderect(self.image_box.get()) and m_rect.colliderect(self.left_box.get()):
            pg.mouse.set_cursor(pgl.SYSTEM_CURSOR_SIZEWE)

        elif m_rect.colliderect(self.image_box.get()) and \
                m_rect.colliderect(self.preview_box.get()):

            pg.mouse.set_cursor(pgl.SYSTEM_CURSOR_SIZENS)

        else:
            pg.mouse.set_cursor(pgl.SYSTEM_CURSOR_ARROW)

    def render_debug(self):
        ...

    def render(self):
        cr.renderer.draw_color = colors.CRIMSON
        cr.renderer.draw_rect(self.top_box.get())
        cr.renderer.draw_rect(self.bottom_box.get())

        cr.renderer.draw_color = colors.FOREST_GREEN
        cr.renderer.draw_rect(self.log_box.get())
        cr.renderer.draw_rect(self.left_box.get())
        cr.renderer.draw_rect(self.info_box.get())

        cr.renderer.draw_color = colors.NAVY
        cr.renderer.draw_rect(self.image_box.get())
        cr.renderer.draw_rect(self.detail_box.get())
        cr.renderer.draw_rect(self.preview_box.get())

        if cr.event_holder.should_render_debug:
            self.render_debug()







# todo: find the purpose of DetailedView.log_box box & choose a better name
