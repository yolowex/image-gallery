from common.names import *
import common.resources as cr
from core.event_holder import EventHolder
import common.constants as constants
from core.log import Log

class Entry:
    def __init__(self,log:Log):
        pg.init()
        flags = RESIZABLE | SCALED
        cr.screen = pg.display.set_mode([800,600],flags)
        cr.window = Window.from_display_module()
        cr.log = log
        """
        _sdl2 is a hidden pygame module, therefore the linters can't find it
        and converse with it properly. to fix annoying false alarms, we use # noqa here,
        which disables any linter errors and warnings
        """
        cr.window.position = pg._sdl2.video.WINDOWPOS_CENTERED # noqa
        cr.renderer = pg._sdl2.video.Renderer.from_window(cr.window) # noqa

        cr.event_holder = EventHolder()

        local_apps_data = os.environ.get('LOCALAPPDATA')

        if local_apps_data is not None:
            app_data_path = local_apps_data+f"/{constants.APP_NAME}"
            log_path = app_data_path + "/log.json"
            if not os.path.exists(app_data_path):
                os.mkdir(app_data_path)
        else:
            app_data_path = constants.APP_DATA_PATH
            log_path = constants.LOG_PATH


        constants.init_constants()
        constants.LOG_PATH = log_path
        constants.APP_DATA_PATH = app_data_path



    def run( self ):
        while not cr.event_holder.should_quit:
            cr.renderer.draw_color = Color("gray")
            cr.renderer.clear()
            cr.event_holder.get_events()
            cr.renderer.present()



