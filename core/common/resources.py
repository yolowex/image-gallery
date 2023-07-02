from core.common.names import *
from core.event_holder import EventHolder
from core.log import Log
from core.mouse import Mouse

event_holder: Optional[EventHolder] = None

window: Optional[Window] = None
renderer: Optional[Renderer] = None
log: Optional[Log] = None

mouse: Optional[Mouse] = None
gallery = None
editor = None


def ws() -> Vector2:
    """
    returns the size of the sdl2 window

    :return: Vector2
    """
    # todo: handle this linter error
    return Vector2(window.size)
