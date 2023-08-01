from enum import Enum


class TaskEnum(Enum):
    FAIL = "fail"
    SUCCESS = "success"
    PENDING = "pending"


class LogLevel(Enum):
    DEBUG = 0
    ANNOUNCE = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5


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

    PILLOW = [
        "bmp",
        "jpeg",
        "jpg",
        "png",
        "tiff",
        "gif",
        "psd",
        "webp",
        "ico",
        "tga",
        "pbm",
        "pgm",
        "ppm",
        "hdr",
        "svg",
    ]

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

    ALL = -1
    DIR = 0
    FILE = 1
    FILE_PIC = 2
    FILE_GIF = 3
    FILE_MOV = 4


class SelectedInfoView(Enum):
    FOLDERS = 0
    TAGS = 1
    EDIT = 2


class ClipboardEnum(Enum):
    COPY = 0
    CUT = 1
    DELETE = 2
    CREATE_FOLDER = 3
    RENAME = 4


class ClipboardResultEnum(Enum):
    PENDING = 0
    RUNNING = 1
    FAILED = 2
    SUCCESS = 3


class Alignment(Enum):
    LEFT = -1
    CENTER = 0
    RIGHT = 1


SelectedInfoView_All = [
    SelectedInfoView.FOLDERS,
    SelectedInfoView.TAGS,
    SelectedInfoView.EDIT,
]
