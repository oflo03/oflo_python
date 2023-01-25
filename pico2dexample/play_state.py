import game_framework
import itembox_state
from pico2d import *
from boy import Boy
from grass import Grass

boy = None
grass = None
running = None

def enter():
    global boy, grass, running
    boy = Boy()
    grass = Grass()
    running = True

def exit():
    global boy, grass, item_image
    del boy
    del grass

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        boy.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_e:
                game_framework.push_state(itembox_state)

def update():
    boy.update()
    delay(0.1)

def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()