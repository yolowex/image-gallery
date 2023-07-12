from core.common.names import *

import cv2
import numpy
from moviepy.editor import VideoFileClip
import threading
import tempfile
# Get the video file
video_path = '/home/yolo/Videos/backup2/quleditor.mp4'
video_path = '/home/yolo/Series/oshi-no-ko/Oshi no Ko - 03.[SS][1080][AioFilm.com].mkv'
opencv_video = cv2.VideoCapture(video_path)

moviepy_video = VideoFileClip(video_path)
moviepy_audio = moviepy_video.audio

temp_audio_file = None
done_loading = False
def make_temp_sound_file():
    global temp_audio_file,done_loading
    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=True)
    moviepy_audio.write_audiofile(temp_audio_file.name,fps=22050)
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
audio_codec = int(opencv_video.get(cv2.CAP_PROP_FOURCC))

# init the mixer
# pg.mixer.init(audio_codec)
# load the audio from the video and play

pg.mixer.music.load(video_path)
pg.mixer.music.play()
# pg.mixer.init()
# s = pg.mixer.Sound(video_path)
# print(s,s.get_length())
# s.play()

is_playing = False
the_audio = None
while run:

    if done_loading and not is_playing:
        pg.mixer.music.load(temp_audio_file.name)
        pg.mixer.music.play()

        is_playing = True

    # Get next frame
    for i in pg.event.get():
        if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
            run = False
            thread1.join()
            break

        if i.type == pgl.KEYDOWN:
            if i.key == pgl.K_RETURN:
                # print(opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000,pg.mixer.music.get_pos())
                current_vid = opencv_video.get(cv2.CAP_PROP_POS_MSEC) / 1000
                # print(pg.mixer.music.get_pos(),(current_vid + 5))
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

        # Convert it to pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        surface = pg.surfarray.make_surface(frame)
        texture.update(surface)

        size = ws()
        rect = FRect(0,0,size.x,size.y)
        # renderer.draw_color = Color("black")
        # renderer.clear()
        texture.draw(None,rect,flip_x=True)



    renderer.present()
    clock.tick(fps)



thread1.join()
# result = os.remove(temp_audio_file.name)
# print(result)