from pico2d import *
import random

open_canvas(1460, 816)
hide_cursor()

background = load_image('background.png')
player = load_image('player.png')
mouse = load_image('mouse-pointer.png')

running = True
iscomposite = False
size = 3
cnt = 0
frame_cnt = 0
xframe, yframe = 100, 55
player_x, player_y = 730, 260
xspeed, yspeed = 0, 0
mouse_x, mouse_y = 730, 260

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False


def draw():
    global running
    global iscomposite
    global size
    global cnt
    global frame_cnt
    global xframe, yframe
    global player_x, player_y
    global xspeed, yspeed
    global mouse_x, mouse_y
    background.draw_now(730, 408, 1460, 816)
    if 0 == xspeed and 0 == yspeed:
        if iscomposite:
            player.clip_composite_draw(xframe * frame_cnt, yframe * 8, xframe, yframe, 0, 'h', player_x, player_y, xframe * size, yframe * size)
        else:
            player.clip_draw(xframe * frame_cnt, yframe * 8, xframe, yframe, player_x, player_y, xframe * size, yframe * size)
        if 0 == cnt % 4:
            frame_cnt = (frame_cnt + 1) % 8
    else:
        if iscomposite:
            player.clip_composite_draw(xframe * (frame_cnt + 8 if frame_cnt < 2 else frame_cnt - 2), yframe * (8 if frame_cnt < 2 else 7), xframe, yframe, 0, 'h', player_x, player_y, xframe * size, yframe * size)
        else:
            player.clip_draw(xframe * (frame_cnt + 8 if frame_cnt < 2 else frame_cnt - 2), yframe * (8 if frame_cnt < 2 else 7), xframe, yframe, player_x, player_y, xframe * size, yframe * size)
        if 0 == cnt % 4:
            frame_cnt = (frame_cnt + 1) % 10
    cnt += 1
    mouse.draw(mouse_x + 10, mouse_y - 16)
    update_canvas()

while running:
    handle_events()
    if abs(player_x - mouse_x) < 10 and abs(player_y - mouse_y < 16):
        mouse_x,mouse_y = random.randrange(1460), random.randrange(816)
        time = ((mouse_x - player_x)**2+(mouse_y - player_y)**2)**0.5 / 7
        xspeed, yspeed = (mouse_x - player_x)/time, (mouse_y - player_y)/time
        if mouse_x - player_x < 0: iscomposite = True
        else: iscomposite = False
    player_x += xspeed
    player_y += yspeed

    clear_canvas()
    draw()

    delay(0.03)

close_canvas()
