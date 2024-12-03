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
            Beam.image = load_image('flash.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_width = 250 / 6

    def draw(self):
        frame_width = 219 / 6  # 각 프레임의 가로 너비
        frame_x = int(self.frame) * int(frame_width)  # 현재 프레임의 시작 x 좌표
        self.image.clip_draw(frame_x, 0, int(frame_width), 439, self.x, self.y, 200, 1000)
        draw_rectangle(*self.get_bb())

    def update(self):
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= 6:
            print("Removing beam object")
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - (250/6), self.y - 800, self.x + (250/6), self.y + 800

    def handle_collision(self, group, other):
        if group == 'player:attack':
            pass


