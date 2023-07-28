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

        # 0, 1,3
        self.brightness = 0.5
        # 0, 1,3
        self.contrast = 0.5
        # 0, 1,3
        self.saturation = 0.5
        # 0, 1,3
        self.sharpness = 0.5

        # 0, 1,3
        self.highlight = 0.5

        # 0, 1,3
        self.red = 0.5
        # 0, 1,3
        self.green = 0.5
        # 0, 1,3
        self.blue = 0.5

    def print_fields(self):
        # Use dir() to get all the names (fields) in the current scope (class)
        fields = dir(self)

        # Filter out the special Python attributes (those starting with __)
        filtered_fields = [field for field in fields if not field.startswith("__")]

        # Print the field names and their corresponding values
        for field in filtered_fields:
            value = getattr(self, field)
            print(f"{field}: {value}")

    def formula_1(self, val, mod=2, left_bound=0.0):
        # return val * 2
        if val < 0.5:
            return utils.lerp(left_bound, 1, val * 2)
        else:
            return utils.lerp(1, mod, (val - 0.5) * 2)

    def perform(self):
        self.print_fields()
        img = self.content.pillow_image

        f = self.formula_1
        img = putils.rotate_and_flip_image(img, self.angle, self.flip_x, False)
        img = putils.modify_color_balance(
            img, f(self.red, 5), f(self.green, 5), f(self.blue, 5)
        )

        img = putils.modify_brightness(img, f(self.brightness, 3))
        img = putils.modify_contrast(img, f(self.contrast, 5, 0.025))

        img = putils.modify_sharpness(img, f(self.sharpness, 5, -5))
        img = putils.modify_saturation(img, f(self.saturation))

        self.content.modified_image = img
        self.content.surface = utils.open_image_to_pygame_surface(
            image=self.content.modified_image
        )

        self.content.texture = Texture.from_surface(cr.renderer, self.content.surface)
