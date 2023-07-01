from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import Colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils

class ZoomView:
    def __init__(self,container_box:RelRect,image:Texture):
        self.container_box = container_box
        self.image = image
        self.inner_image_rect = FRect(0,0,0,0)

    def update(self):

        # self.inner_image_rect = self.container_box.get_in_rect(Vector2(self.image.get_rect().size))
        self.inner_image_rect = self.container_box.get_in_rect(Vector2(100,100))


    def check_events(self):
        # rect = self.box.init_rect.copy()
        # rect.x += self.container_box.rect.x
        # rect.y += self.container_box.rect.y
        #
        # self.box.rect = rect
        ...

    def render_debug(self):
        ...

    def render(self):

        self.image.draw(None,self.inner_image_rect)



        if cr.event_holder.should_render_debug:
            self.render_debug()

