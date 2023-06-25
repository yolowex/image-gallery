from common.names import *
import platform

# Determine the platform
current_platform = platform.system()

# Set the boolean variables based on the platform
IS_WINDOWS = (current_platform == 'Windows')
IS_LINUX = (current_platform == 'Linux')
IS_MAC = (current_platform == 'Darwin')

# Print the platform
print("Current platform: ", current_platform)

if IS_WINDOWS:
    version_info = platform.win32_ver()
    release_version = version_info[0]
    service_pack = version_info[1]
    build_number = version_info[2]

    print("Release Version:", release_version)
    print("Service Pack:", service_pack)
    print("Build Number:", build_number)

elif IS_LINUX:
    # Get distribution information
    distribution = \
    subprocess.check_output(['lsb_release', '-d']).decode('utf-8').strip().split('\t')[1]
    print("Distribution:", distribution)

    # Get kernel version
    kernel_version = subprocess.check_output(['uname', '-r']).decode('utf-8').strip()
    print("Kernel Version:", kernel_version)

elif IS_MAC:

    version_info = platform.mac_ver()
    macos_version = version_info[0]
    build_number = version_info[1]

    print("macOS Version:", macos_version)
    print("Build Number:", build_number)
else:
    print("Warning: running on an unknown platform")