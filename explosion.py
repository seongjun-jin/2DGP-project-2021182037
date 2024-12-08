from pico2d import load_image, draw_rectangle, load_font
import game_framework
from Boss1 import boss

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class explosion:
    def __init__(self):
        self.x, self.y = 600, 60
        self.image = load_image("explosion.png")
        self.is_guide = False
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.is_guide = False

    def draw(self):
        if self.image:
            self.image.clip_draw(int(self.frame) * 58, 120, 58, 65, self.x, self.y, 50, 50)


