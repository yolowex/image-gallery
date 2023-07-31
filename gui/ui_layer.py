from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from gui.button import Button
from helper_kit.relative_rect import RelRect
from core.common import utils


class UiLayer:
    def __init__(self):
        self.buttons: list[Button] = []
        self.any_hovered = False

    def check_events(self):
        self.any_hovered = False

        for button in self.buttons:
            button.check_events()
            if button.is_hovered:
                self.any_hovered = True
                break

    def render(self):
        for button in self.buttons:
            button.render()
