from asyncio import Runner
from logging import root

import server
from pico2d import *
import game_framework
import random
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import time
import math
from fireball import fireball
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
        self.Max_hp = 5
        self.font = load_font('ENCR10B.TTF', 16)
        self.is_hit = False
        self.is_hit_timer = 0
        self.face_dir = 1
        self.speed = 5
        self.tx, self.ty = 0,0
        self.is_beaten = False
        self.build_behavior_tree()
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
        if self.bt:
            self.bt.run()



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
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time * 10
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

        self.x = clamp(50, self.x, 700)
        self.y = clamp(50, self.y, 500)

    def distance_less_than(self, x1, y1, x2, y2, r):
            distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
            return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_to_left_up(self):
            self.tx, self.ty = 25, 600
            self.move_slightly_to(self.tx, self.ty)
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, 7):
                if not hasattr(self, 'wait_start'):
                    self.wait_start = time.time()  # 대기 시작 시간 기록
                elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                    del self.wait_start  # 대기 완료 후 초기화
                    return BehaviorTree.SUCCESS
                return BehaviorTree.RUNNING
            return BehaviorTree.RUNNING


    def move_to_right_up(self):
        self.tx, self.ty = 800, 600
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 7):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.RUNNING

    def move_to_left_down(self):
        self.tx, self.ty = 25, 25
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 7):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.RUNNING

    def move_to_right_down(self):
        self.tx, self.ty = 800, 25
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 7):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.RUNNING

    def move_to_center(self):
        self.tx, self.ty = 400, 300
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 7):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.RUNNING

    def split_fire_ball(self):
        """보스의 위치에서 여러 방향으로 파이어볼 발사"""
        num_fireballs = 8  # 파이어볼 개수
        angle_step = 2 * math.pi / num_fireballs  # 360도 나누기 파이어볼 개수
        speed = 20  # 파이어볼 속도

        for i in range(num_fireballs):
            angle = i * angle_step  # 각 파이어볼의 발사 각도 계산
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            # 파이어볼 생성
            fireball_obj = fireball(self.x, self.y, velocity_x, velocity_y)

            # game_world에 추가
            game_world.add_object(fireball_obj, 1)
            game_world.add_collision_pair('player:attack', None, fireball_obj)
        return BehaviorTree.SUCCESS


    def fireball_rain(self): #하늘에서 불비가 내려옴

        pass
    def split_in_center(self): #화면중앙에서 360도로 파이어볼 발사
        pass
    def move_and_fire(self): #왼쪽위-> 오른쪽위-> 오른쪽아래->왼쪽 아래로 이동해 추적하는 파이어볼 1기씩 생성
        pass
    def fire_wave(self): #거대한 파이어볼을 떨어뜨려 불의 파도를 만듦
        pass
    def final_flash(self): #거대한 빔 발사
        pass
    def break_time(self): #쉼
        pass

    def build_behavior_tree(self):
        # 각 행동을 Action 노드로 래핑
        a1 = Action('왼쪽 위로 이동', self.move_to_left_up)
        a2 = Action('오른쪽 위로 이동', self.move_to_right_up)
        a3 = Action('왼쪽 아래로 이동', self.move_to_left_down)
        a4 = Action('오른쪽 아래로 이동', self.move_to_right_down)
        a5 = Action('가운데로 이동', self.move_to_center)

        a6 = Action('파이어볼 발사', self.split_fire_ball)
        a7 = Action('파이어볼 발사', self.split_fire_ball)
        a8 = Action('파이어볼 발사', self.split_fire_ball)
        a9 = Action('파이어볼 발사', self.split_fire_ball)
        # Sequence 노드에 Action 리스트 추가

        #pattern 1 불발사
        move_and_fire1 = Sequence('왼쪽 위 이동 + 발사', a1, a6)
        move_and_fire2 = Sequence('오른쪽 위 이동 + 발사', a2, a7)
        move_and_fire3 = Sequence('왼쪽 아래 이동 + 발사', a3, a8)
        move_and_fire4 = Sequence('오른쪽 아래 이동 + 발사', a4, a9)

        #pattern 2 불비


        # 이동-발사 패턴을 순서대로 실행
        root = Sequence('배회 후 발사', move_and_fire1, move_and_fire2, move_and_fire3, move_and_fire4)

        # BehaviorTree에 루트 설정
        self.bt = BehaviorTree(root)
