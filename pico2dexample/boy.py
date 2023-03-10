from pico2d import *
import game_framework

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = PIXEL_PER_METER * RUN_SPEED_MPS

TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10
TIME_PER_IDLE = 0.5
IDLE_PER_TIME = 1.0 / TIME_PER_IDLE
FRAMES_PER_IDLE = 3

class IDLE:
    def enter(self, event):
        self.dir = 0
        self.frame = 0
        self.timer = 0.0
        #if event == RU:
        #    self.face_dir = 1
        #elif event == LU:
        #    self.face_dir = -1
        pass

    def exit(self):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_IDLE * IDLE_PER_TIME * game_framework.frame_time ) % FRAMES_PER_IDLE
        self.timer += game_framework.frame_time
        if self.timer > 5:
            self.event_que.insert(0, 'TIMER5')
        pass

    def draw(self):
        if self.face_dir == -1:
            Boy.idle.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)
        elif self.face_dir == 1:
            Boy.idle.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        pass

class RUN:
    def enter(self, event):
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1
        pass

    def exit(self):
        self.face_dir = self.dir
        pass

    def do(self):
        self.frame = (self.frame + ACTION_PER_TIME * game_framework.frame_time * FRAMES_PER_ACTION) % FRAMES_PER_ACTION
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 800)
        pass

    def draw(self):
        if self.dir == -1:
            Boy.image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)
        elif self.dir == 1:
            Boy.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        pass

class SLEEP:
    def enter(self, event):
        pass

    def exit(self):
        pass

    def do(self):
        #self.event_que.insert(0, 'HIT')
        pass

    def draw(self):
        if self.face_dir == -1:
            Boy.idle.clip_composite_draw(200, 0, 100, 100, 0.5 * math.pi, 'h', self.x, self.y, 100, 100)
        elif self.face_dir == 1:
            Boy.idle.clip_composite_draw(200, 0, 100, 100, -0.5 * math.pi, '', self.x, self.y, 100, 100)
        pass

RD, LD, RU, LU = range(4)
key_event_table = {
(SDL_KEYDOWN, SDLK_RIGHT): RD,
(SDL_KEYDOWN, SDLK_LEFT): LD,
(SDL_KEYUP, SDLK_RIGHT): RU,
(SDL_KEYUP, SDLK_LEFT): LU
}
table = {
'SLEEP': {'HIT': 'WAKE'},
'WAKE': {'TIMER5': 'SLEEP'}
}
next_state = {
IDLE: {RD: RUN, LD: RUN, RU: RUN, LU: RUN, 'TIMER5': SLEEP},
RUN: {RD: IDLE, LD: IDLE, RU: IDLE, LU: IDLE},
SLEEP: {RD: RUN, LD: RUN, RU: RUN, LU: RUN, 'HIT': IDLE}
}


class Boy:
    image = None
    idle = None
    def __init__(self):
        if Boy.image == None:
            Boy.image = load_image('run_animation.png')
        if Boy.idle == None:
            Boy.idle = load_image('ch_idle.png')
        self.x, self.y = 30, 90
        self.dir, self.face_dir = 0, 1
        self.frame = 0
        self.item_image = None
        self.font = load_font('ENCR10B.TTF', 16)

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            self.event_que.insert(0, key_event_table[(event.type, event.key)])

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time():.2f})', (255, 255, 0))