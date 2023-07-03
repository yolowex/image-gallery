from core.common.enums import LogLevel
from core.common.names import *
import core.common.resources as cr

pics: list[Texture] = []
ui_buttons: Dict[str,Texture] = {}

def init_assets():
    global pics,ui_buttons

    cr.log.write_log("Loading the test_assets from disk...",LogLevel.DEBUG)

    pics = [
        Texture.from_surface(
            cr.renderer, pg.image.load(os.path.abspath("./test_assets/" + i))
        )
        for i in os.listdir(os.path.abspath("./test_assets"))
    ]


    expected_ui_buttons = 12

    ui_buttons_path = os.path.abspath("./assets/ui-buttons")
    # this might fail on windows
    ui_buttons_path_list = [ui_buttons_path+"/"+i for i in os.listdir(ui_buttons_path)]

    c = 0
    fail_to_load = False
    for path in ui_buttons_path_list:
        # this too

        try:
            file = path.split("/")[-1]
            name,extension = file.split(".")
            surface = pg.image.load(path)
            texture = Texture.from_surface(cr.renderer,surface)
            ui_buttons[name] = texture

        except Exception as e:
            fail_to_load = True
            cr.log.write_log(f"Warning: Could not load {path} due to {e} error"
                , LogLevel.FATAL)

        c+=1



    if c < expected_ui_buttons:
        cr.log.write_log("Warning! some of the assets could not be found!"
                         " the app will probably close unexpectedly!", LogLevel.FATAL)

    elif c > expected_ui_buttons:
        cr.log.write_log("Warning! the assets folder was tempered with!"
                         " the app will probably close unexpectedly!", LogLevel.ERROR)

    else:
        if not fail_to_load:
            cr.log.write_log("All of the assets are found and loaded successfully!",LogLevel.DEBUG)


    if fail_to_load:
        cr.log.write_log("Warning! some of the assets could not be loaded!"
                         " the app will probably close unexpectedly!", LogLevel.FATAL)
