from core.clipboard import Clipboard
from core.common.names import *
from core.event_holder import EventHolder
from core.log import Log
from core.mouse import Mouse
from core.common.themes import ColorThemes

event_holder: Optional[EventHolder] = None

window: Optional[Window] = None
renderer: Optional[Renderer] = None
log: Optional[Log] = None

mouse: Optional[Mouse] = None
gallery = None
editor = None

sql_agent = None

clipboard = Clipboard()

color_theme = ColorThemes()


def ws() -> Vector2:
    """
    returns the size of the sdl2 window

    :return: Vector2
    """
    # todo: handle this linter error
    return Vector2(window.size)


def ws_rect() -> FRect:
    """
    returns the rectangle of the sdl2 window

    :return: Vector2
    """
    return FRect((0, 0), window.size)
