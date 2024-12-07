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


class fireball:
    image = None

    def __init__(self, x, y, velocity_x, velocity_y):
        if fireball.image is None:
            fireball.image = load_image('voidball.png')  # 파이어볼 이미지 로드
        self.x = x
        self.y = y
        self.velocity_x = velocity_x  # X 방향 속도
        self.velocity_y = velocity_y  # Y 방향 속도
        self.frame = 0

    def draw(self):
        self.image.clip_draw(0, 0, 73, 59, self.x, self.y, 80, 80)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14

    def get_bb(self):
        return self.x - 33, self.y - 33, self.x + 33, self.y + 33

    def handle_collision(self, group, other):
        if group == 'player:attack':
            game_world.remove_object(self)


