from core.common.names import *
import core.common.resources as cr

class Mouse:
    def __init__(self):
        self.current_cursor: int = pgl.SYSTEM_CURSOR_ARROW

    def check_events(self):

        pg.mouse.set_cursor(self.current_cursor)
        self.current_cursor = pg.SYSTEM_CURSOR_ARROW
