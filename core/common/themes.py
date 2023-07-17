from enum import Enum
import core.common.constants as constants
from pygame import Color


class colors:
    """
    why are you repeating yourself? :/
    answer: circular import problems ( aka bad programming )
    """

    GLASS = Color([0, 0, 0, 0])

    # Basic Colors
    WHITE = Color([255, 255, 255])
    BLACK = Color([0, 0, 0])

    # Primary Colors
    RED = Color([255, 0, 0])
    GREEN = Color([0, 255, 0])
    BLUE = Color([0, 0, 255])

    # Secondary Colors
    YELLOW = Color([255, 255, 0])
    ORANGE = Color([255, 165, 0])
    PURPLE = Color([128, 0, 128])

    # Other Popular Colors
    PINK = Color([255, 192, 203])
    GRAY = Color([128, 128, 128])
    BROWN = Color([165, 42, 42])
    MAGENTA = Color([255, 0, 255])
    CYAN = Color([0, 255, 255])
    LIME = Color([0, 255, 0])
    NAVY = Color([0, 0, 128])
    TEAL = Color([0, 128, 128])
    OLIVE = Color([128, 128, 0])
    MAROON = Color([128, 0, 0])

    # Metallic Colors
    GOLD = Color([255, 215, 0])
    SILVER = Color([192, 192, 192])

    # Shades and Tints
    INDIGO = Color([75, 0, 130])
    AQUA = Color([0, 255, 255])
    CORAL = Color([255, 127, 80])
    SKY_BLUE = Color([135, 206, 235])
    LAVENDER = Color([230, 230, 250])
    TURQUOISE = Color([64, 224, 208])
    ORCHID = Color([218, 112, 214])
    SALMON = Color([250, 128, 114])
    BEIGE = Color([245, 245, 220])

    # Additional Colors
    STEEL_BLUE = Color([70, 130, 180])
    CHOCOLATE = Color([210, 105, 30])
    PLUM = Color([221, 160, 221])
    DARK_GREEN = Color([0, 100, 0])
    CRIMSON = Color([220, 20, 60])
    PALE_GREEN = Color([152, 251, 152])
    HOT_PINK = Color([255, 105, 180])
    MEDIUM_ORCHID = Color([186, 85, 211])
    DARK_SLATE_GRAY = Color([47, 79, 79])
    SPRING_GREEN = Color([0, 255, 127])
    FOREST_GREEN = Color([34, 139, 34])
    NEON = Color(150, 180, 255)
    # GIMP colors
    GIMP_0 = Color("#3b3b3b")
    GIMP_1 = Color("#454545")
    GIMP_2 = Color("#5c5c5c")


class ColorThemes:
    class Pattern(Enum):
        DARK = [
            Color("#3b3b3b"),  # color_0
            Color("#454545"),  # color_1
            Color("#5c5c5c"),  # color_2
            Color(150, 180, 255),  # button
            Color([255, 255, 255]),  # text_0
            Color([200, 200, 200]),  # text_1
            Color([64, 224, 208]),  # navigator
            colors.RED,  # error
            colors.OLIVE,  # selected box
            colors.BEIGE,  # scroll bar border
            colors.CHOCOLATE.lerp("black", 0.5),  # navigator border
        ]

        LIGHT = [
            i.lerp(Color("white"), 0.3)
            for i in [
                Color("#3b3b3b"),
                Color("#454545"),
                Color("#5c5c5c"),
                Color(150, 180, 255),
                Color([255, 255, 255]),
                Color([200, 200, 200]),
                Color([64, 224, 208]),
                colors.RED,
                colors.OLIVE,
                colors.BEIGE,
                colors.CHOCOLATE.lerp("black", 0.5),
            ]
        ]

        MEXICO = [
            i.lerp(Color("orange"), 0.1)
            for i in [
                Color("#3b3b3b"),
                Color("#454545"),
                Color("#5c5c5c"),
                Color(150, 180, 255),
                Color([255, 255, 255]),
                Color([200, 200, 200]),
                Color([64, 224, 208]),
                colors.RED,
                colors.OLIVE,
                colors.BEIGE,
                colors.CHOCOLATE.lerp("black", 0.5),
            ]
        ]

        NEON = [
            i.lerp(Color("blue"), 0.3).lerp(Color("black"), 0.5)
            for i in [
                Color("#3b3b3b"),
                Color("#454545"),
                Color("#5c5c5c"),
                Color(150, 180, 255),
                Color([255, 255, 255]),
                Color([200, 200, 200]),
                Color([64, 224, 208]),
                colors.RED,
                colors.OLIVE,
                colors.BEIGE,
                colors.CHOCOLATE.lerp("black", 0.5),
            ]
        ]

    DARK = Pattern.DARK
    LIGHT = Pattern.LIGHT
    MEXICO = Pattern.MEXICO
    NEON = Pattern.NEON

    ALL = [DARK, LIGHT, MEXICO, NEON]

    __index = 0

    def __init__(self):
        self.current_theme: ColorThemes.Pattern = ColorThemes.Pattern.DARK

    def go_next(self):
        ct = ColorThemes
        ct.__index += 1
        if ct.__index == len(ct.ALL):
            ct.__index = 0

        self.current_theme = ct.ALL[ct.__index]

    @property
    def color_0(self):
        return self.current_theme.value[0]

    @property
    def color_1(self):
        return self.current_theme.value[1]

    @property
    def color_2(self):
        return self.current_theme.value[2]

    @property
    def button(self):
        return self.current_theme.value[3]

    @property
    def text_0(self):
        return self.current_theme.value[4]

    @property
    def text_1(self):
        return self.current_theme.value[5]

    @property
    def navigator(self):
        return self.current_theme.value[6]

    @property
    def error(self):
        return self.current_theme.value[7]

    @property
    def selection(self):
        return self.current_theme.value[8]

    @property
    def scroll_bar_border(self):
        return self.current_theme.value[9]

    @property
    def navigator_bar_border(self):
        return self.current_theme.value[10]
