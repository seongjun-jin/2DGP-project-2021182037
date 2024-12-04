from pico2d import *
import game_world
import game_framework
import Boss1

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Beam:
    image = None

    def __init__(self, x, y):
        if Beam.image is None:
            Beam.image = load_image('flash2.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_width = 250 / 6

    def draw(self):
        frame_width = 189 / 6  # 각 프레임의 가로 너비
        self.image.clip_draw(int(self.frame) * int(frame_width), 0, int(frame_width), 419, self.x + 50, self.y - 1025, 300, 2000)
        draw_rectangle(*self.get_bb())

    def update(self):
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.frame >= 5:
            print("Removing beam object")
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 3* (189/6), self.y - 800, self.x + 3*(189/6), self.y + 600

    def handle_collision(self, group, other):
        if group == 'player:attack':
            pass


