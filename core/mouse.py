from core.common.names import *
import core.common.resources as cr

class Mouse:
    def __init__(self):
        self.current_cursor: int = pgl.SYSTEM_CURSOR_ARROW

    def request_mouse_cursor(self,mouse_cursor:int):
        ...

    def check_events(self):
        ...