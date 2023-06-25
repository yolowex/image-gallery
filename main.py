from common.names import *
import common.resources as cr
from core.event_holder import EventHolder
import common.constants as constants
pg.init()



flags = RESIZABLE | SCALED

cr.screen = pg.display.set_mode([800,600],flags)
cr.window = Window.from_display_module()
"""
_sdl2 is a hidden pygame module, therefore the linters can't find it
and converse with it properly. to fix annoying false alarms, we use # noqa here,
which disables any linter error and warning
"""
cr.window.position = pg._sdl2.video.WINDOWPOS_CENTERED # noqa
cr.renderer = pg._sdl2.video.Renderer.from_window(cr.window) # noqa

cr.event_holder = EventHolder()

while not cr.event_holder.should_quit:
    cr.renderer.draw_color = Color("gray")
    cr.renderer.clear()
    cr.event_holder.get_events()
    cr.renderer.present()



