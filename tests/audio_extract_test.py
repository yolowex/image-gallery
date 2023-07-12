import subprocess
import os

in_video_path =  os.path.abspath("../test_assets/movie.mkv")

bin_path = os.path.abspath("../ffmpeg/bin/ffmpeg.exe")
out_audio_path =  os.path.abspath("../dump/audio3.mp3")

command = f"{bin_path} -i {in_video_path} -vn -acodec libmp3lame -qscale:a 2 {out_audio_path}"

output = subprocess.run(command,shell=True,capture_output=True)
print(output)