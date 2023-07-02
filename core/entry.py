from core.common import assets
from core.common.names import *
import core.common.resources as cr
from core.editor.editor import Editor
from core.event_holder import EventHolder
import core.common.constants as constants
from core.log import Log
from core.gallery.gallery import Gallery
from core.mouse import Mouse


class Entry:
    def __init__(self, log: Log):
        pg.init()

        # todo: fix the bug/problem with borderless flag breaking the resizable flag
        cr.window = Window(size=[700, 700], resizable=True,borderless=True)
        cr.log = log
        """
        _sdl2 is a hidden pygame module, therefore the linters can't find it
        and converse with it properly. to fix annoying false alarms, we use # noqa here,
        which disables any linter errors and warnings
        """
        cr.window.position = pg._sdl2.video.WINDOWPOS_CENTERED  # noqa
        cr.renderer = Renderer(cr.window)
        cr.mouse = Mouse()
        cr.event_holder = EventHolder()

        current_platform = platform.system()

        app_name = "Foto Folio"
        app_data_path = "."
        if current_platform == "Windows":
            x = os.environ.get("LOCALAPPDATA")
            if x is not None:
                app_data_path = x

        app_data_path = f"{app_data_path}/{app_name}"
        log_path = os.path.abspath(f"{app_data_path}/log.json")

        if not os.path.exists(app_data_path):
            os.mkdir(app_data_path)

        constants.init_constants()
        constants.LOG_PATH = log_path
        constants.APP_DATA_PATH = app_data_path

        assets.init_assets()

        cr.gallery = Gallery()
        cr.editor = Editor()

    def run(self):
        while not cr.event_holder.should_quit:
            cr.renderer.draw_color = Color("gray")
            cr.renderer.clear()
            cr.event_holder.get_events()
            cr.gallery.check_events()
            cr.mouse.check_events()
            cr.gallery.render()
            cr.renderer.present()
