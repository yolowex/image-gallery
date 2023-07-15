from core.common.enums import LogLevel
from core.log import Log
import platform
import traceback
import os

import os
import pathlib
import sys

print(f"current working directory is {os.getcwd()}\n")
print(sys.argv)

file_path = pathlib.Path(sys.argv[0]).resolve().as_posix()
file_name = file_path.split("/")[-1]
file_path = file_path[: len(file_path) - len(file_name) - 1]
print(f"entry file is located at: {file_path}\n")
print(f"changing the cwd to {file_path}\n")
if file_path != "":
    os.chdir(file_path)

print(f"current working directory is {os.getcwd()}\n")


current_platform = platform.system()
app_name = "Foto Folio"
app_data_path = "."
if current_platform == "Windows":
    x = os.environ.get("LOCALAPPDATA")
    if x is not None:
        app_data_path = x

app_data_path = f"{app_data_path}/{app_name}"
log_path = os.path.abspath(f"{app_data_path}/log.json")

print(f"The log file is located at {log_path}")

if not os.path.exists(app_data_path):
    os.mkdir(app_data_path)

log = Log(log_path)
error = False
try:
    log.write_log("Starting the app...", LogLevel.INFO)
    from core.entry import Entry

    entry = Entry(log)
    entry.run()

except Exception as e:
    error_log = "Unexpected error: " + str(e) + "\n" + traceback.format_exc()
    log.write_log(error_log, LogLevel.FATAL)
    error = True


log.write_log("Closing the app...", LogLevel.INFO)
if error:
    input("Press any key to exit")
