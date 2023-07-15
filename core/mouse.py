from core.common.names import *
import core.common.resources as cr


class Mouse:
    def __init__(self):
        self.current_cursor: int = pgl.SYSTEM_CURSOR_ARROW
        self.high_priority_cursor: Optional[int] = None

    def set_high_priority(self, cursor):
        self.high_priority_cursor = cursor

    def check_events(self):
        # unsafe: there's not telling if data has any items
        cur = pg.mouse.get_cursor().data[0]

        if self.high_priority_cursor is not None:
            if cur != self.high_priority_cursor:
                pg.mouse.set_cursor(self.high_priority_cursor)
                # print('setting cursor, high priority',cur,self.high_priority_cursor)
        else:
            if cur != self.current_cursor:
                pg.mouse.set_cursor(self.current_cursor)
                # print('setting cursor',cur,self.current_cursor)

        self.current_cursor = pg.SYSTEM_CURSOR_ARROW
