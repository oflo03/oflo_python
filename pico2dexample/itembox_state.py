from pico2d import *
import game_framework
import  play_state

running = True
image = None

def enter():
    global image
    image = load_image('item_state.png')

def exit():
    global image
    del image

def update():
    pass

def draw():
    global image
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif event.key == SDLK_0:
                play_state.boy.item_image = None
            elif event.key == SDLK_1:
                play_state.boy.item_image = load_image('ball21X21.png')
            elif event.key == SDLK_2:
                play_state.boy.item_image = load_image('ball41X41.png')
