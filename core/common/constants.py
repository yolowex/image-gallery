from core.common import utils
from core.common.enums import LogLevel
from core.common.names import *
import core.common.resources as cr
import platform

SUPPORTED_FILE_FORMATS = [
    "png",
    "jpg",
    "jpeg",
    "tiff",
    "gif",
    "webp",
    "avi",
    "mp4",
    "mpeg",
    "mkv",
    "mov",
    "wmv",
    "flv",
]

APP_NAME = "Foto Folio"
APP_DATA_PATH = ""
LOG_PATH = ""


LOCAL_APPS_DATA = ""
IS_WINDOWS = False
IS_LINUX = False
IS_MAC = False
WINDOWS_RELEASE_VERSION = ""
WINDOWS_SERVICE_PACK = ""
WINDOWS_BUILD_NUMBER = ""
LINUX_DISTRIBUTION = ""
LINUX_KERNEL_VERSION = ""
MACOS_VERSION = ""
MACOS_BUILD_NUMBER = ""
MACOS_ARCHITECTURE = ""

DISPLAY_SIZE = None
DISPLAY_ASPECT_RATIO = None

def export_platform_constants():
    global IS_WINDOWS, WINDOWS_BUILD_NUMBER, WINDOWS_SERVICE_PACK, WINDOWS_RELEASE_VERSION
    global IS_LINUX, LINUX_DISTRIBUTION, LINUX_KERNEL_VERSION
    global IS_MAC, MACOS_VERSION, MACOS_BUILD_NUMBER, MACOS_ARCHITECTURE
    global LOCAL_APPS_DATA
    global DISPLAY_SIZE,DISPLAY_ASPECT_RATIO


    inf = pg.display.Info()
    DISPLAY_SIZE = Vector2(
        inf.current_w,
        inf.current_h
    )

    DISPLAY_ASPECT_RATIO = utils.get_aspect_ratio(DISPLAY_SIZE)

    current_platform = platform.system()

    IS_WINDOWS = current_platform == "Windows"
    IS_LINUX = current_platform == "Linux"
    IS_MAC = current_platform == "Darwin"

    cr.log.write_log("Current platform: " + current_platform, LogLevel.INFO)

    if IS_WINDOWS:
        version_info = platform.win32_ver()
        WINDOWS_RELEASE_VERSION = version_info[0]
        WINDOWS_SERVICE_PACK = version_info[1]
        WINDOWS_BUILD_NUMBER = version_info[2]
        LOCAL_APPS_DATA = os.environ.get("LOCALAPPDATA")

        cr.log.write_log("Release Version:" + WINDOWS_RELEASE_VERSION, LogLevel.INFO)
        cr.log.write_log("Service Pack:" + WINDOWS_SERVICE_PACK, LogLevel.INFO)
        cr.log.write_log("Build Number:" + WINDOWS_BUILD_NUMBER, LogLevel.INFO)

    elif IS_LINUX:
        LINUX_DISTRIBUTION = (
            subprocess.check_output(["lsb_release", "-d"])
            .decode("utf-8")
            .strip()
            .split("\t")[1]
        )
        cr.log.write_log("Distribution:" + LINUX_DISTRIBUTION, LogLevel.INFO)

        LINUX_KERNEL_VERSION = (
            subprocess.check_output(["uname", "-r"]).decode("utf-8").strip()
        )
        cr.log.write_log("Kernel Version:" + LINUX_KERNEL_VERSION, LogLevel.INFO)

    elif IS_MAC:
        mac_version = platform.mac_ver()

        MACOS_VERSION = mac_version[0]
        MACOS_BUILD_NUMBER = mac_version[1]
        MACOS_ARCHITECTURE = mac_version[2]

        cr.log.write_log("macOS Version:" + MACOS_VERSION, LogLevel.INFO)
        cr.log.write_log("Build Number:" + str(MACOS_BUILD_NUMBER), LogLevel.INFO)
        cr.log.write_log("Architecture:" + MACOS_ARCHITECTURE, LogLevel.INFO)

    else:
        cr.log.write_log("Warning: running on an unknown platform", LogLevel.INFO)


class colors:
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


"""
I added this try/except block just in case, it might be unnecessary thou
"""


def init_constants():
    try:
        export_platform_constants()
    except Exception as e:
        # Print the traceback and error message
        error_log = (
            "Could not fetch platform details due to this error! :"
            + str(e)
            + "\n"
            + traceback.format_exc()
        )
        cr.log.write_log(error_log, LogLevel.ERROR)
