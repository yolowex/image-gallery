from core.common import assets, utils
from core.common.names import *
import core.common.resources as cr
from core.event_holder import EventHolder
import core.common.constants as constants
from core.log import Log
from core.gallery.gallery import Gallery
from core.mouse import Mouse
from core.sql_agent import SqlAgent


class Entry:
    def __init__(self, log: Log):
        pg.init()

        # todo: fix the bug/problem with borderless flag breaking the resizable flag
        cr.window = Window(
            title=f"{constants.APP_NAME}", size=[700, 700], resizable=True
        )
        cr.log = log
        """
        _sdl2 is a hidden pygame module, therefore the linters can't find it
        and converse with it properly. to fix annoying false alarms, we use # noqa here,
        which disables any linter errors and warnings
        """
        cr.window.position = pg._sdl2.video.WINDOWPOS_CENTERED  # noqa
        cr.sql_agent = SqlAgent()
        cr.renderer = Renderer(cr.window)
        cr.mouse = Mouse()
        cr.event_holder = EventHolder()
        # todo: test the fps in windows
        cr.event_holder.determined_fps = 200

        icon = pg.image.load("./assets/icon.png")
        cr.window.set_icon(icon)

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

        constants.TEMPDIR = constants.APP_DATA_PATH + "/tmp"

        if not os.path.exists(constants.TEMPDIR):
            os.mkdir(constants.TEMPDIR)

        assets.init_assets()
        cr.sql_agent.init()

        cr.gallery = Gallery()
        cr.gallery.init()
        utils.init()

    def run(self):
        while not cr.event_holder.should_quit:
            cr.renderer.draw_color = Color(constants.colors.GIMP_2)
            cr.renderer.clear()
            cr.event_holder.get_events()
            cr.gallery.check_events()
            cr.mouse.check_events()
            cr.gallery.render()
            cr.renderer.present()
