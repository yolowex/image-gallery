import pygame as pg
from pygame.locals import *


pg.init()
music = pg.mixer_music
screen = pg.display.set_mode([1, 1], NOFRAME)
music.load("../test_assets/music.mp3")
music.play()
music.set_volume(0.5)
run = True

paused = False
stopped = False

print_data = lambda *x: print(start_time, paused, stopped, music.get_pos(), *x)
step = 5
start_time = 0
while run:
    for i in pg.event.get():
        if i.type == QUIT or i.type == KEYDOWN and i.key == K_ESCAPE:
            run = False

        if i.type == KEYDOWN:
            k = i.key
            if k == K_SPACE:
                paused = not paused
                if paused:
                    music.pause()
                    print_data("pause")
                else:
                    music.unpause()
                    print_data("unpause")

            if k == K_RETURN:
                stopped = not stopped
                if stopped:
                    music.stop()
                    print_data("stop")
                else:
                    music.play()
                    print_data("play")

            if k == K_RIGHT:
                print_data("before going right")
                pos = start_time + music.get_pos() / 1000
                pos += step
                start_time = pos

                music.stop()
                music.play(start=start_time)
                # music.rewind()
                # music.set_pos(step)
                print_data("after going right\n")

            if k == K_LEFT:
                print_data("before going right")
                pos = start_time + music.get_pos() / 1000
                pos -= step
                start_time = pos
                if start_time < 0:
                    start_time = 0
                # music.rewind()
                # music.set_pos(-step)
                music.stop()
                music.play(start=start_time)
                print_data("after going right\n")

            if k == K_f:
                print_data()
