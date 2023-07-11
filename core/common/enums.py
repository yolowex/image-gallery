from enum import Enum


class TaskEnum(Enum):
    FAIL = "fail"
    SUCCESS = "success"
    PENDING = "pending"


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4


class ViewType(Enum):
    FULLSCREEN = 0
    DETAILED = 1


class AspectRatioGroup(Enum):
    # todo: find a better name for the rectangular group
    RECTANGULAR = 0
    PORTRAIT = 1
    LANDSCAPE = 2


class ContentSourceType(Enum):
    """
    this enum class maps every supported file format to 3 different
    libraries that can load them. all of them are eventually converted
    into a pygame.Surface, and then a pygame.__sdl2.Texture, so native
    pygame type extensions are obviously loaded faster

    """

    PYGAME = ["png", "jpg", "jpeg", "tiff", "bmp", "tga"]
    PILLOW = ["gif", "webp"]
    OPENCV = ["avi", "mp4", "mpeg", "mkv", "mov", "wmv", "flv"]


class ContentType(Enum):
    PICTURE = 0
    GIF = 1
    VIDEO = 2


class FileType(Enum):
    """
    this is a helper enum class for FolderView,
    it's job is to distinguish the different file and directory types here.
    """

    DIR = 0
    FILE = 1
    FILE_PIC = 2
    FILE_GIF = 3
    FILE_MOV = 4


class SelectedInfoView(Enum):
    FOLDERS = 0
    INFO = 1
    EDIT = 2


SelectedInfoView_All = [
    SelectedInfoView.FOLDERS,
    SelectedInfoView.INFO,
    SelectedInfoView.EDIT,
]
