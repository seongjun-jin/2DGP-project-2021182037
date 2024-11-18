from pico2d import load_image, draw_rectangle
import game_world
import game_framework
from Boss1 import boss

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Slash:
    image = None
    def __init__(self, x = 400, y = 300, face_dir = 1):
        if Slash.image == None:
            Slash.image = load_image('slash.png')
        self.x, self.y, self.frame, self.dir = x, y, 0, face_dir
        self.attacker = None
        self.is_attacking = False

    def draw(self):

        if self.frame < (FRAMES_PER_ACTION - 1):
            if self.dir == 1:
                self.image.clip_draw(int(self.frame)*(500//6), 0, (500//6), 100, self.x + 60, self.y + 10, 150, 50)
            if self.dir == -1:
                self.image.clip_composite_draw(int(self.frame) * (500 // 6), 0, (500 // 6), 100, 0, 'h', self.x - 60, self.y + 10, 150, 50)
        elif self.frame >= (FRAMES_PER_ACTION - 1):
            game_world.remove_object(self)
            self.is_attacking = False
            print(f'self.is_attacking = {self.is_attacking}')
            boss.is_hit = False
            print(f'boss.is_hit = {boss.is_hit}')
            if self.attacker:
                self.attacker.is_attacking = False
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % FRAMES_PER_ACTION

        pass


    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        if self.dir == 1:
            return self.x + 10, self.y - 10, self.x + 120, self.y + 20
        if self.dir == -1:
            return self.x - 120, self.y - 10, self.x - 10, self.y + 20
        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'boss:attack':
            self.is_attacking = True
            pass