from common.names import *
import platform



IS_WINDOWS = ""
IS_LINUX = ""
IS_MAC = ""
WINDOWS_RELEASE_VERSION = ""
WINDOWS_SERVICE_PACK = ""
WINDOWS_BUILD_NUMBER = ""
LINUX_DISTRIBUTION = ""
LINUX_KERNEL_VERSION = ""
MACOS_VERSION = ""
MACOS_BUILD_NUMBER = ""
MACOS_ARCHITECTURE = ""

def export_platform_constants() :
    # inline globalization does not work prior to python 3.6 version
    global IS_WINDOWS,WINDOWS_BUILD_NUMBER,WINDOWS_SERVICE_PACK,WINDOWS_RELEASE_VERSION
    global IS_LINUX,LINUX_DISTRIBUTION,LINUX_KERNEL_VERSION
    global IS_MAC,MACOS_VERSION,MACOS_BUILD_NUMBER,MACOS_ARCHITECTURE


    # Determine the platform
    current_platform = platform.system()

    # Set the boolean variables based on the platform
    IS_WINDOWS = (current_platform == 'Windows')
    IS_LINUX = (current_platform == 'Linux')
    IS_MAC = (current_platform == 'Darwin')

    # Print the platform
    print("Current platform: ", current_platform)


    if IS_WINDOWS :
        version_info = platform.win32_ver()
        WINDOWS_RELEASE_VERSION = version_info[0]
        WINDOWS_SERVICE_PACK = version_info[1]
        WINDOWS_BUILD_NUMBER = version_info[2]

        print("Release Version:", WINDOWS_RELEASE_VERSION)
        print("Service Pack:", WINDOWS_SERVICE_PACK)
        print("Build Number:", WINDOWS_BUILD_NUMBER)

    elif IS_LINUX :
        # Get distribution information
        LINUX_DISTRIBUTION = \
            subprocess.check_output(['lsb_release', '-d']).decode('utf-8').strip().split('\t')[1]
        print("Distribution:", LINUX_DISTRIBUTION)

        # Get kernel version
        LINUX_KERNEL_VERSION = subprocess.check_output(['uname', '-r']).decode('utf-8').strip()
        print("Kernel Version:", LINUX_KERNEL_VERSION)

    elif IS_MAC :
        mac_version = platform.mac_ver()

        MACOS_VERSION = mac_version[0]
        MACOS_BUILD_NUMBER = mac_version[1]
        MACOS_ARCHITECTURE = mac_version[2]

        print("macOS Version:", MACOS_VERSION)
        print("Build Number:", MACOS_BUILD_NUMBER)
        print("Architecture:", MACOS_ARCHITECTURE)

    else :
        print("Warning: running on an unknown platform")


"""
    I added this try/except block just in case, it might be unnecessary thou
"""
try:
    export_platform_constants()
except Exception as e:
    # Print the traceback and error message
    print("Could not fetch platform details due to this error! :", str(e),file=sys.stderr)
    traceback.print_exc()
