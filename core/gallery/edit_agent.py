from core.common import utils
from core.common.enums import LogLevel
from core.common.names import *
import core.common.resources as cr
import core.common.constants as constants
import core.common.pillow_utils as putils


class EditAgent:
    def __init__(self, content):
        self.content = content

        self.angle = 0
        self.flip_x = False

        self.brightness = 0.5
        self.contrast = 0.5
        self.saturation = 0.5
        self.sharpness = 0.5

        self.highlight = 0.5
        self.shadow = 0.5

        self.red = 0.5
        self.green = 0.5
        self.blue = 0.5

    def __str__(self):
        return f"{self.angle}-{self.flip_x}-{self.brightness}"

    def perform(self):
        img = self.content.pillow_image

        img = putils.rotate_and_flip_image(img, self.angle, self.flip_x, False)
        img = putils.modify_color_balance(img, self.red, self.green, self.blue)

        img = putils.modify_brightness(img, self.brightness)
        img = putils.modify_contrast(img, self.contrast)

        img = putils.modify_sharpness(img, self.sharpness)
        img = putils.modify_saturation(img, self.saturation)
        img = putils.adjust_shadow_highlight(img, self.shadow, self.highlight)

        self.content.modified_image = img
        self.content.surface = utils.open_image_to_pygame_surface(
            image=self.content.modified_image
        )

        self.content.texture = Texture.from_surface(cr.renderer, self.content.surface)
