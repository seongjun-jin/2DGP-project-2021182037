from pico2d import *
import game_framework
import random
#
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8




class boss:
    def __init__(self):
        self.x, self.y = 400,200
        self.frame = 0
        self.image = load_image("1.png")
        self.hp = 5
        self.font = load_font('ENCR10B.TTF', 16)
        self.is_hit = False
        self.is_hit_timer = 0
        self.face_dir = 1
        self.is_beaten = False
        self.pattern1 = False
        self.pattern2 = False
        self.pattern3 = False
        self.pattern4 = False
        self.pattern5 = False
        self.pattern = random.randint(0,4)
        if self.image is None:
            print("Image failed to load")

    def handle_event(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 8
        if self.is_hit:  # 일정 시간 후 다시 충돌 가능
            self.is_hit_timer -= game_framework.frame_time
            if self.is_hit_timer <= 0:
                self.is_hit = False
        if self.hp == 0:
            self.is_beaten = True

    def draw(self):
        if not self.is_beaten:
            self.image.clip_draw(self.frame * 75, 2700, 75, 105, self.x, self.y)
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x - 10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        else:
            self.is_beaten = True
            pass

    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'boss:player':
            pass
        elif group == 'boss:attack'and not self.is_hit and other.is_attacking:
            self.hp -= 1
            self.is_hit = True
            self.is_hit_timer = 0.5