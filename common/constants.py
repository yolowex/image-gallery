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
    print("Running on Windows")
elif IS_LINUX:
    print("Running on Linux")
elif IS_MAC:
    print("Running on macOS")
else:
    print("Running on an unknown platform")