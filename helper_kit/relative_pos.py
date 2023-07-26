from core.common.enums import *
from core.common.names import *
from core.common import utils
import core.common.resources as cr


class RelPos:
    def __init__(self, pos: Vector2, source_function):
        self.pos = pos
        self.source_function = source_function

    def get(self):
        return self.source_function(self.pos)
