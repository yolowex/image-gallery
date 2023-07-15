# standard
import os
import sys
import time
import random
import subprocess
import traceback
import json
import datetime
import pathlib
import platform

from typing import Optional, List, Dict, Union

# third party
import pygame as pg
import pygame.locals as pgl
from pygame import Color, Font, FRect, Vector2, Surface

from pygame._sdl2 import Renderer, Texture, Window  # noqa

import numpy
import cv2
from moviepy.editor import VideoFileClip
import threading
# Get the video file

ffmpeg_path = '"' + os.path.abspath('../ffmpeg/bin/ffmpeg.exe') + '"'
video_path = os.path.abspath('../test_assets/clip.avi')
opencv_video = cv2.VideoCapture(video_path)

tempdir = "./tmp"
if not os.path.exists(tempdir):
    os.mkdir(tempdir)

if platform.system() == "Linux":
    ffmpeg_path = 'ffmpeg'

moviepy_video = VideoFileClip(video_path)
moviepy_audio = moviepy_video.audio

temp_audio_file = None
done_loading = False

def write_audiofile(in_video_path,out_audio_path,ffmpeg_path) -> bool:

    command = f"{ffmpeg_path} -y -i \"{in_video_path}\" -vn " \
                            f"-acodec libmp3lame -qscale:a 2 \"{out_audio_path}\""
    result = True
    try:
        subprocess.check_call(command, shell=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}.")
        result = False

    return result

def make_temp_sound_file():
    global temp_audio_file,done_loading
    temp_audio_file = "./tmp/test.mp3"
    if not write_audiofile(video_path,temp_audio_file,ffmpeg_path):
        raise OSError("Could not make the temp file")
    # moviepy_audio.write_audiofile(temp_audio_file.name,fps=22050)
    done_loading = True


thread1 = threading.Thread(target=make_temp_sound_file)
thread1.start()


screen_width = int(opencv_video.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(opencv_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

pg.init()


window = Window(size=[700, 700], resizable=True)

window.position = pg._sdl2.video.WINDOWPOS_CENTERED  # noqa
renderer = Renderer(window)

ws = lambda: Vector2(window.size)

texture = Texture(renderer,(screen_width,screen_height))
run = True
clock = pg.time.Clock()
fps = opencv_video.get(cv2.CAP_PROP_FPS)
opencv_video.set(cv2.CAP_PROP_POS_MSEC, 0)
total_time = opencv_video.get(cv2.CAP_PROP_FRAME_COUNT) / fps



is_playing = False
the_audio = None

now = lambda: pg.time.get_ticks() / 1000
timer = now()
duration = 10

while run:

    if done_loading and not is_playing:
        pg.mixer.music.load(temp_audio_file)
        pg.mixer.music.play()

        is_playing = True

    if is_playing:
        if now() > timer + duration :
            current_vid = opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000
            pg.mixer.music.set_pos(current_vid)
            timer = now()
            print('syncing')

    # Get next frame
    for i in pg.event.get():
        if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
            run = False
            thread1.join()
            break


        if i.type == pgl.KEYDOWN:
            if i.key == pgl.K_RETURN:
                current_vid = opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000

                pg.mixer.music.rewind()
                pg.mixer.music.set_pos(7)



            if i.key == pgl.K_RIGHT:
                step = 5
                current_vid = opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000
                opencv_video.set(cv2.CAP_PROP_POS_MSEC, (current_vid + step)*1000 )

                current_aud = pg.mixer.music.get_pos() / 1000
                last_pos = pg.mixer.music.get_pos()
                pg.mixer.music.rewind()
                pg.mixer.music.set_pos(current_vid+step)
                new_pos = pg.mixer.music.get_pos()
                print(last_pos,new_pos)

            if i.key == pgl.K_LEFT:
                step = 5
                current_vid = opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000
                opencv_video.set(cv2.CAP_PROP_POS_MSEC, (current_vid - step) * 1000)

                current_aud = pg.mixer.music.get_pos() / 1000
                last_pos = pg.mixer.music.get_pos()
                pg.mixer.music.rewind()
                pg.mixer.music.set_pos(current_vid - step)
                new_pos = pg.mixer.music.get_pos()
                print(last_pos, new_pos)



    renderer.draw_color = Color(185,185,220)
    renderer.clear()

    if done_loading:
        ret, frame = opencv_video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        surface = pg.surfarray.make_surface(frame)
        texture.update(surface)

        size = ws()
        rect = FRect(0,0,size.x,size.y)

        texture.draw(None,rect,flip_x=True)



    renderer.present()
    clock.tick(fps)



thread1.join()
