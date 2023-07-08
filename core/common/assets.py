import pygame

from core.common.enums import LogLevel
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content

ui_buttons: Dict[str, Texture] = {}
test_assets_path = os.path.abspath("./test_assets")
assets_path = os.path.abspath("./assets")
content_placeholder: Optional[Content] = None
fonts = {}


def init_assets():
    global ui_buttons, content_placeholder


    fonts["mid"] = pg.font.SysFont("monospace",25)

    content_placeholder = Content(path=assets_path + "/no_image.png")
    content_placeholder.load()
    # unsafe

    cr.log.write_log("Loading the assets from disk...", LogLevel.DEBUG)

    expected_ui_buttons = 12

    ui_buttons_path = os.path.abspath("./assets/ui-buttons")
    # this might fail on windows
    ui_buttons_path_list = [
        ui_buttons_path + "/" + i for i in os.listdir(ui_buttons_path)
    ]

    c = 0
    fail_to_load = False
    for path in ui_buttons_path_list:
        # this too

        try:
            file = path.split("/")[-1]
            name, extension = file.split(".")
            surface = pg.image.load(path)
            texture = Texture.from_surface(cr.renderer, surface)
            ui_buttons[name] = texture

        except Exception as e:
            fail_to_load = True
            cr.log.write_log(
                f"Warning: Could not load {path} due to {e} error", LogLevel.FATAL
            )

        c += 1

    if c < expected_ui_buttons:
        cr.log.write_log(
            "Warning! some of the assets could not be found!"
            " the app will probably close unexpectedly!",
            LogLevel.FATAL,
        )

    elif c > expected_ui_buttons:
        cr.log.write_log(
            "Warning! the assets folder was tempered with!"
            " the app will probably close unexpectedly!",
            LogLevel.ERROR,
        )

    else:
        if not fail_to_load:
            cr.log.write_log(
                "All of the assets are found and loaded successfully!", LogLevel.DEBUG
            )

    if fail_to_load:
        cr.log.write_log(
            "Warning! some of the assets could not be loaded!"
            " the app will probably close unexpectedly!",
            LogLevel.FATAL,
        )
