from pico2d import *

open_canvas(960,544)

background = load_image('background.png')
player = load_image('player.png')

xframe = 100
yframe = 55
size = 3
x = 0
cnt = 0

while (x < 960):
    clear_canvas()
    background.draw_now(480, 272)
    player.clip_draw(xframe * (cnt + 8 if cnt < 2 else cnt - 2), yframe * (8 if cnt < 2 else 7), xframe, yframe, x, 140,xframe * size, yframe * size)
    update_canvas()
    cnt = (cnt + 1) % 10
    x += 20
    delay(0.08)

close_canvas()
