from core.common.names import *
from core.common.utils import *


pg.init()
screen = pg.display.set_mode([800, 600])

run = True

w, h = screen.get_size()
con_rect = FRect(w * 0.2, h * 0.2, w * 0.6, h * 0.6)
rect = FRect(0, 0, w * 0.3, h * 0.3)


while run:
    for i in pg.event.get():
        if i.type == pgl.QUIT or i.type == pgl.KEYDOWN and i.key == pgl.K_ESCAPE:
            run = False

    screen.fill("gray")

    temp_rect = rect.copy()
    temp_rect.center = pg.mouse.get_pos()
    cut_rect = cut_rect_in(con_rect, temp_rect)

    pg.draw.rect(screen, Color("blue"), cut_rect)
    pg.draw.rect(screen, Color("red"), temp_rect, 3)
    pg.draw.rect(screen, Color("black"), con_rect, 3)

    pg.display.update()
