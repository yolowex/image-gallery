from core.common.names import *
import core.common.resources as cr

pics: list[Texture] = []


def init_assets() :
    global pics
    pics = [Texture.from_surface(cr.renderer, pg.image.load("./test_assets/" + i)) for i in
        os.listdir("./test_assets")]
