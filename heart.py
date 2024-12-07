from pico2d import load_image, load_font, draw_rectangle
import game_framework
import math
import server
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Heart:
    def __init__(self):
        self.x = 500
        self.y = 70
        self.image = load_image('warning_sign_heart.png')
        self.frame = 0
        self.motion = 0  # 움직임 제어를 위한 변수
        self.direction = 1  # 위(1) 또는 아래(-1)로 움직이는 방향
        self.amplitude = 10  # 움직임의 범위 (픽셀)
        self.speed = 2  # 움직임 속도
        self.is_guide = False
        self.effected_one = None
        self.removed = False
        self.item_font = load_font('강원교육튼튼.ttf', 32)
        self.guide_font = load_font('강원교육튼튼.ttf', 15)

    def draw(self):
        if self.image and not server.player.item_select:
            if self.is_guide:
                self.image.clip_draw(0, 0, 192, 187, self.x, self.y, 50, 50)
                self.guide_font.draw(self.x - 100, self.y + 50, f'아래 방향키로 획득(아이템 2개 중 하나만 선택 가능합니다)', (0, 0, 0))
                self.item_font.draw(0, 500, f'플레이어의 최대 체력을 1 늘립니다', (0,0,0))

            else:
                self.image.clip_draw(0, 0, 192, 187, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def update(self):
        # 프레임 업데이트
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.is_guide = False
        # y 좌표를 위아래로 움직임
        self.motion += self.speed
        self.y += math.sin(self.motion * 0.1) * self.amplitude * game_framework.frame_time
        self.effected_one = None
        if server.player.item_select and not self.removed:
            game_world.remove_object(self)


    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        pass

    def handle_collision(self, group, other):
        if group == 'player:item':
            self.is_guide = True
            self.effected_one = other

    def apply_effect(self, player):
        if not server.player.item_select:
            if not self.removed:
                player.MAX_hp += 1
                player.hp = min(player.MAX_hp, player.hp + 1)  # 체력을 최대값으로 회복
                print(f"Sword effect applied! attack_force increased to {player.attack_force}")
                #game_world.remove_object(self)
                self.removed = True
                server.player.item_select = True



