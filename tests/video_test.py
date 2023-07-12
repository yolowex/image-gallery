from core.common.names import *

import cv2
import numpy

# Get the video file
vid = cv2.VideoCapture('/home/yolo/Series/oshi-no-ko/Oshi no Ko - 03.[SS][1080][AioFilm.com].mkv')

# Set screen size and create display
screen_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

pg.init()

# todo: fix the bug/problem with borderless flag breaking the resizable flag
window = Window(size=[700, 700], resizable=True)

window.position = pg._sdl2.video.WINDOWPOS_CENTERED  # noqa
renderer = Renderer(window)

ws = lambda: Vector2(window.size)

texture = Texture(renderer,(screen_width,screen_height))
run = True
clock = pg.time.Clock()
fps = vid.get(cv2.CAP_PROP_FPS)

while run:
    # Get next frame
    for i in pg.event.get():
        if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
            run = False
            break

    ret, frame = vid.read()

    # Convert it to pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = numpy.rot90(frame)
    surface = pg.surfarray.make_surface(frame)
    texture.update(surface)

    size = ws()
    rect = FRect(0,0,size.x,size.y)
    # renderer.draw_color = Color("black")
    # renderer.clear()
    texture.draw(None,rect)

    renderer.present()
    clock.tick(fps)

    # Display the frame

