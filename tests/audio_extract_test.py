import subprocess
import os

in_video_path =  os.path.abspath("../test_assets/clip.mp4")

bin_path = os.path.abspath("../ffmpeg/bin/ffmpeg.exe")
out_audio_path =  os.path.abspath("../dump/audio3.mp3")

command = f"{bin_path} -y -i {in_video_path} -vn -acodec libmp3lame -qscale:a 2 {out_audio_path}"

try:
    subprocess.check_call(command, shell=True)
    print("Command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}.")