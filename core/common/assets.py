from core.common.names import *
import core.common.resources as cr

pics: list[Texture] = []


def init_assets():
    global pics
    pics = [
        Texture.from_surface(
            cr.renderer, pg.image.load(os.path.abspath("./test_assets/" + i))
        )
        for i in os.listdir(os.path.abspath("./test_assets"))
    ]
