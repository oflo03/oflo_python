from pico2d import *
import game_framework
import itembox_state

boy = None
grass = None
running = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.item_image = None

    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        if self.item_image:
            self.item_image.draw(self.x, self.y + 50)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_e:
                game_framework.push_state(itembox_state)

def enter():
    global boy, grass, running
    boy = Boy()
    grass = Grass()
    running = True

def exit():
    global boy, grass, item_image
    del boy
    del grass

def update():
    boy.update()
    delay(0.05)

def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass