from core.common import utils
from core.common.names import *
import core.common.resources as cr


class Mouse:
    def __init__(self):
        self.current_cursor: int = pgl.SYSTEM_CURSOR_ARROW
        self.high_priority_cursor: Optional[int] = None
        self.virtual_cursor = Vector2(0, 0)

    def set_high_priority(self, cursor):
        self.high_priority_cursor = cursor

    @property
    def is_virtual(self):
        return utils.is_enabled_virtual_mouse()

    def enable_virtual(self):
        # self.virtual_cursor.update(0,0)
        return utils.enable_virtual_mouse()

    def disable_virtual(self):
        # self.virtual_cursor.update(0,0)
        return utils.disable_virtual_mouse()

    def check_events(self):
        # unsafe: there's not telling if data has any items
        cur = pg.mouse.get_cursor().data[0]

        if self.is_virtual and cr.event_holder.mouse_moved:
            rel = pg.mouse.get_rel()
            self.virtual_cursor += rel
            print(self.virtual_cursor, rel, cr.event_holder.mouse_pos)

        if self.high_priority_cursor is not None:
            if cur != self.high_priority_cursor:
                pg.mouse.set_cursor(self.high_priority_cursor)
                # print('setting cursor, high priority',cur,self.high_priority_cursor)
        else:
            if cur != self.current_cursor:
                pg.mouse.set_cursor(self.current_cursor)
                # print('setting cursor',cur,self.current_cursor)

        self.current_cursor = pg.SYSTEM_CURSOR_ARROW
