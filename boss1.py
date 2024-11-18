from pico2d import *
import game_framework
import random
import game_world
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
        self.speed = 5
        self.is_beaten = False
        self.pattern0 = True
        self.pattern1 = False
        self.pattern2 = False
        self.pattern3 = False
        self.pattern4 = False
        self.pattern5 = False
        self.pattern_count = 0
        self.pattern = 0
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
        if self.pattern0 == True:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.x += RUN_SPEED_PPS * self.face_dir * game_framework.frame_time * self.speed
            if self.x >= 800:
                self.face_dir = -1
                self.speed -= 1
                if self.x == 800:
                    self.speed = 0

            elif self.x <= 0:
                self.face_dir = 1
                self.speed -= 1
                if self.x == 0:
                    self.speed = 0

            if  self.speed == 0:
                self.speed = 5



    def draw(self):
        if not self.is_beaten:
            if self.face_dir == 1:
                self.image.clip_draw(int(self.frame) * 75, 2700, 75, 105, self.x, self.y,100,100)
            elif self.face_dir == -1:
                self.image.clip_composite_draw((int(self.frame) * 75), 2700, 75, 105, 0,'h',self.x, self.y,100,100)
            draw_rectangle(*self.get_bb())
            self.font.draw(self.x - 10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        else:
            self.is_beaten = True
            game_world.remove_object(self)
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

    def boss_pattern(self):
        if self.pattern == 0:
            self.pattern0 = True
            self.pattern1 = False
            self.pattern2 = False
            self.pattern3 = False
            self.pattern4 = False
            self.pattern = random.randint(0, 4)
            self.pattern_count += 1

        elif self.pattern == 1:
            self.pattern0 = False
            self.pattern1 = True
            self.pattern2 = False
            self.pattern3 = False
            self.pattern4 = False
            self.pattern = random.randint(0, 4)
            self.pattern_count += 1

        elif self.pattern == 2:
            self.pattern0 = False
            self.pattern1 = False
            self.pattern2 = True
            self.pattern3 = False
            self.pattern4 = False
            self.pattern = random.randint(0, 4)
            self.pattern_count += 1

        elif self.pattern == 3:
            self.pattern0 = False
            self.pattern1 = False
            self.pattern2 = False
            self.pattern3 = True
            self.pattern4 = False
            self.pattern = random.randint(0, 4)
            self.pattern_count += 1

        elif self.pattern == 4:
            self.pattern0 = False
            self.pattern1 = False
            self.pattern2 = False
            self.pattern3 = False
            self.pattern4 = True
            self.pattern = random.randint(0, 4)
            self.pattern_count += 1

        if self.pattern_count == 5:
            self.pattern0 = False
            self.pattern1 = False
            self.pattern2 = False
            self.pattern3 = False
            self.pattern4 = False
            self.pattern5 = True
            self.pattern_count = 0
            self.pattern = random.randint(0, 4)