from pico2d import load_image, draw_rectangle, load_font
import server
from Portal import portal
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

class hp_bar:
    def __init__(self):
        self.x, self.y = 600, 60
        self.image = load_image("hp_bar.png")
        self.hp_ratio = 1.0  # Start with full HP
        self.hp_width = 364 / 4

    def update(self):
        if hasattr(server, 'boss') and hasattr(server.boss, 'hp') and hasattr(server.boss, 'Max_hp'):
            self.hp_ratio = server.boss.hp / server.boss.Max_hp
        else:
            self.hp_ratio = 1.0  # Default full HP if boss is not defined

    def draw(self):
        if self.image and server.players_map == 'bossroom1':  # Adjust as needed
            self.image.clip_draw(0, self.hp_width * 4, 678, self.hp_width, 200, 700, 100, 100)