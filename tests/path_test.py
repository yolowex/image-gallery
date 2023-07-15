import os
import pathlib

print(f"current working directory is {os.getcwd()}\n")


file_path = pathlib.Path(__file__).resolve().as_posix()
file_name = file_path.split("/")[-1]
file_path = file_path[:len(file_path)-len(file_name)-1]
print(f"entry file is located at: {file_path}\n")
print(f"changing the cwd to {file_path}\n")
os.chdir(file_path)

print(f"current working directory is {os.getcwd()}\n")


input()