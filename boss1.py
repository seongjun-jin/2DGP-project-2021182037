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
from beam import Beam
from dark_hand import hand
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

class explosion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image("explosion.png")
        self.width = 1054 / 7
        self.height = 223
        self.frame = 0
        self.timer = 0

    def update(self):
        self.timer += game_framework.frame_time
        if self.timer > 0.1:  # 0.1초마다 다음 프레임으로
            self.frame += 1
            self.timer = 0
        if self.frame >= 7:  # 마지막 프레임까지 재생되면 삭제
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(
            int(self.frame) * int(self.width), 0, int(self.width), int(self.height),
            self.x, self.y, 100, 100
        )
class hp_bar:
    def __init__(self, boss):
        self.hp_ratio = None
        self.boss = boss
        self.hp_image = load_image("hp.png")
        self.back_image = load_image("hp_bar.png")
        self.hp_width = 588  # 초기 너비 설정
        self.x, self.y = 400, 580  # HP 바 위치

    def update(self, hp, max_hp):
        self.hp_ratio = hp / max_hp if max_hp > 0 else 0
        self.hp_width = 588 * self.hp_ratio  # HP 비율에 따라 너비 조정
        print(f"HP Bar Updated: {self.hp_ratio * 100:.1f}%")

    def draw(self):
        # Draw the HP background
        self.back_image.clip_draw(0, 0, 616, 83, self.x, self.y - 40)

        # Draw the HP bar according to current HP
        self.hp_image.clip_draw(0, 0, int(self.hp_width), 30, self.x - (588 - self.hp_width) / 2, self.y - 40)




class boss:
    def __init__(self):
        self.x, self.y = 400,200
        self.hp_bar = None
        self.frame = 0
        self.image = load_image("1.png")
        self.max_hp = 5  # 최대 HP
        #self.current_hp = 100  # 현재 HP
        self.hp = self.max_hp
        self.font = load_font('ENCR10B.TTF', 16)
        self.is_hit = False
        self.is_hit_timer = 0
        self.face_dir = 1
        self.speed = 5
        self.tx, self.ty = 0,0
        #self.is_beaten = False
        self.is_dead = False  # 보스가 죽었는지 확인하는 플래그
        self.death_timer = 0  # 죽는 연출 타이머
        self.explosion_added = False
        self.explosions = []  # 폭발 리스트
        self.explosion_timer = 0  # 폭발 간격 타이머
        self.next_explosion_time = 0.3  # 다음 폭발까지 대기 시간
        self.build_behavior_tree()
        self.screen_shake_intensity = 0  # 흔들림 강도
        self.screen_shake_duration = 0  # 흔들림 지속 시간
        self.shake_start_time = 0  # 흔들림 시작 시간
        if self.image is None:
            print("Image failed to load")
        self.hp_bar = hp_bar(self)  # 여기 추가
        if self.image is None:
            print("Image failed to load")

    def handle_event(self):
        self.frame = 0

    def update(self):
        if self.is_dead:
            # 폭발 이펙트 생성
            self.y = self.y - 1
            self.explosion_timer += game_framework.frame_time

            if self.explosion_timer >= self.next_explosion_time:
                # 보스 주변 무작위 위치에서 폭발 생성
                explosion_x = self.x + random.uniform(-50, 50)
                explosion_y = self.y + random.uniform(-50, 50)
                explosion_obj = explosion(explosion_x, explosion_y)
                game_world.add_object(explosion_obj, 1)
                self.explosions.append(explosion_obj)
                self.explosion_timer = 0  # 타이머 초기화
            # 5초 후 보스 객체 제거
            self.death_timer += game_framework.frame_time
            if self.death_timer > 5.0:
                if self in game_world.world[1]:  # 객체가 존재하는지 확인
                    game_world.remove_object(self)
                else:
                    print("Warning: Attempted to remove a non-existing object.")
                game_framework.screen_color = (0, 0, 0)  # 화면을 원래대로 돌림
            return

        # 보스 HP가 0이면 죽음 상태로 전환
        if self.hp <= 0 and not self.is_dead :
            self.is_dead = True
            game_framework.screen_color = (255, 255, 255)  # 화면을 하얗게 바꿈
            self.death_timer = 0  # 타이머 초기화

        # 보스가 아직 살아있는 경우 기존 로직 실행
        if self.is_hit:
            self.is_hit_timer -= game_framework.frame_time
            if self.is_hit_timer <= 0:
                self.is_hit = False

        self.hp_bar.update(self.hp, self.max_hp)
        self.bt.run()

    def draw(self):
        if self.is_dead:
            #return  # 보스가 죽었으면 그리기를 중지
            pass

        offset_x = game_framework.screen_offset_x
        offset_y = game_framework.screen_offset_y

        if self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 75, 2700, 75, 105,
                                 self.x + offset_x, self.y + offset_y, 100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame) * 75, 2700, 75, 105,
                                           0, 'h', self.x + offset_x, self.y + offset_y, 100, 100)
        self.font.draw(self.x - 10 + offset_x, self.y + 50 + offset_y,
                       f'{self.hp:02d}', (255, 255, 0))

        # HP 바 그리기
        if self.hp_bar:
            self.hp_bar.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
        pass

    def handle_collision(self, group, other):
        if group == 'boss:player':
            print("Collision with player detected!")
            pass
        elif group == 'boss:attack' and not self.is_hit:
            print(f"Collision with attack: {type(other).__name__}, is_attacking: {other.is_attacking}")
            if other.is_attacking:
                self.hp -= 1
                self.is_hit = True
                self.is_hit_timer = 0.5
                print(f"Boss HP reduced to {self.hp}.")

    def start_screen_shake(self, intensity, duration):
        """화면 흔들림 효과를 시작"""
    def move_slightly_to(self, tx, ty):
        if not (0 <= tx <= 800 and 0 <= ty <= 600):
            raise ValueError(f"Invalid target position: tx={tx}, ty={ty}")
        if not (0 <= self.x <= 800 and 0 <= self.y <= 600):
            raise ValueError(f"Invalid current position: x={self.x}, y={self.y}")

        distance_to_target = math.sqrt((tx - self.x) ** 2 + (ty - self.y) ** 2)

        distance_squared = (tx - self.x) ** 2 + (ty - self.y) ** 2
        if distance_squared < 0:
            raise ValueError("Invalid distance: negative value encountered.")
        distance = math.sqrt(distance_squared)

        # 속도 계산: 목표와의 거리에 따라 속도 조정 (멀리 있을수록 빠르게)
        # 최대 속도와 최소 속도 설정
        max_speed = RUN_SPEED_PPS * 10  # 최대 속도 (2배 빠르게)
        min_speed = RUN_SPEED_PPS * 0.2  # 최소 속도 (30% 속도)

        # 속도는 목표와의 거리가 멀수록 빠르고, 가까울수록 느려짐
        if distance_to_target > 200:
            speed = max_speed  # 멀리 있을 때 최대 속도
        elif distance_to_target > 50:
            speed = max_speed * ((distance_to_target / 200) ** 3) # 거리에 따라 속도 비례 감소
        else:
            speed = min_speed  # 매우 가까울 때 최소 속도

        # 이동 방향 계산
        self.dir = math.atan2(ty - self.y, tx - self.x)

        # x, y 이동
        self.x += speed * math.cos(self.dir) * game_framework.frame_time
        self.y += speed * math.sin(self.dir) * game_framework.frame_time

        # 화면 경계 제한
        self.x = clamp(50, self.x, 750)
        self.y = clamp(50, self.y, 550)

    def distance_less_than(self, x1, y1, x2, y2, r):
            distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
            return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_consistently_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_left_up(self):
            self.tx, self.ty = 25, 600
            self.move_slightly_to(self.tx, self.ty)
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
                if not hasattr(self, 'wait_start'):
                    self.wait_start = time.time()  # 대기 시작 시간 기록
                elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                    del self.wait_start  # 대기 완료 후 초기화
                    return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING

    def move_to_right_up(self):
        self.tx, self.ty = 800, 575
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()
            elif time.time() - self.wait_start >= 0.5:
                del self.wait_start
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_to_left_down(self):
        self.tx, self.ty = 25, 25
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_to_right_down(self):
        self.tx, self.ty = 800, 25
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_to_center(self):
        self.tx, self.ty = 400, 300
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_to_upper_center(self):
        self.tx, self.ty = 400, 600
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):
            if not hasattr(self, 'wait_start'):
                self.wait_start = time.time()  # 대기 시작 시간 기록
            elif time.time() - self.wait_start >= 0.5:  # 1초 대기
                del self.wait_start  # 대기 완료 후 초기화
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_to_player(self):
        if not hasattr(self, 'player'):
            self.player = server.player

        tx, ty = self.player.x, self.player.y
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        return BehaviorTree.SUCCESS

    def split_fire_ball(self):
        """보스의 위치에서 여러 방향으로 파이어볼 발사"""
        if not hasattr(self, 'fireball_count'):
            self.fireball_count = 0

        num_fireballs = 8  # 파이어볼 개수
        angle_step = 2 * math.pi / num_fireballs
        speed = 20

        # 발사
        if self.fireball_count < num_fireballs:
            angle = self.fireball_count * angle_step
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            fireball_obj = fireball(self.x, self.y, velocity_x, velocity_y)
            game_world.add_object(fireball_obj, 1)
            game_world.add_collision_pair('player:attack', None, fireball_obj)

            self.fireball_count += 1
            return BehaviorTree.RUNNING

        # 초기화 및 성공 반환
        del self.fireball_count
        return BehaviorTree.SUCCESS

    def fireball_rain(self):  # 하늘에서 불비가 내려옴
        num_failed_fireballs = 10
        fire_step = 100
        speed = -10
        start_x = 400  # 중앙 위치 (필요에 따라 조정)

        for i in range(num_failed_fireballs):
            velocity_y = speed

            # 지그재그 패턴 계산
            if i % 2 == 0:  # 짝수 인덱스: 왼쪽
                x_position = start_x - (fire_step * (i // 2))
            else:  # 홀수 인덱스: 오른쪽
                x_position = start_x + (fire_step * (i // 2))

            y_position = 800  # 고정된 높이 (필요시 변경 가능)

            # Fireball 객체 생성
            fireball_obj = fireball(x_position, y_position, 0, velocity_y)

            # 게임 월드에 객체 추가
            game_world.add_object(fireball_obj, 1)
            game_world.add_collision_pair('player:attack', None, fireball_obj)

        return BehaviorTree.SUCCESS

    def split_in_center(self):
        """12시 방향부터 30도씩 돌아가며 순서대로 발사"""
        if not hasattr(self, 'fireball_angle'):
            self.fireball_angle = 0  # 시작 각도 0도 (12시 방향)
            self.last_fire_time = time.time()  # 마지막 발사 시간 초기화

        # 12발을 30도 간격으로 발사
        if self.fireball_angle < 720:
            current_time = time.time()
            if current_time - self.last_fire_time >= 0.05:  # 발사 간격 (0.2초)
                # 각도를 라디안으로 변환
                angle_radians = math.radians(self.fireball_angle)
                velocity_x = math.cos(angle_radians) * 20
                velocity_y = math.sin(angle_radians) * 20

                # 파이어볼 생성
                fireball_obj = fireball(self.x, self.y, velocity_x, velocity_y)
                game_world.add_object(fireball_obj, 1)
                game_world.add_collision_pair('player:attack', None, fireball_obj)

                # 다음 각도로 이동
                self.fireball_angle += 20
                self.last_fire_time = current_time
            return BehaviorTree.RUNNING
        else:
            # 모든 발사 완료 후 초기화 및 성공 반환
            del self.fireball_angle
            del self.last_fire_time
            return BehaviorTree.SUCCESS

    def fire_wave(self):
        num_hands = 10  # 한 번에 생성되는 손의 수
        hand_spacing = 50  # 손 간의 간격
        start_x = self.x - (num_hands // 2) * hand_spacing  # 손 시작 위치
        y_position = 50  # 손이 처음 나타나는 y 좌표
        warning_timer = 1

        if not hasattr(self, 'wait_start'):
            self.wait_start = time.time()
        elif time.time() - self.wait_start >= warning_timer:
            del self.wait_start
        for i in range(num_hands):
            x_position = start_x + i * hand_spacing  # 손 위치 계산
            hand_obj = hand(x_position, y_position, 0, 0)
            game_world.add_object(hand_obj, 1)
            game_world.add_collision_pair('player:attack', None, hand_obj)

        return BehaviorTree.SUCCESS

    def final_flash(self):
        if not hasattr(self, 'flash_start_time'):
            self.flash_start_time = time.time()

        if time.time() - self.flash_start_time < 0.5:  # 1초 동안 빔 발사 유지
            beam = Beam(self.x, self.y)
            game_world.add_object(beam, 1)
            game_world.add_collision_pair('player:attack', None, beam)
            return BehaviorTree.RUNNING
        else:
            del self.flash_start_time
            return BehaviorTree.SUCCESS

    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 800-100), random.randint(200,600-100)
        return BehaviorTree.SUCCESS

    def warning_sign(self):
        pass

    def move_to(self, r = 0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def break_time(self): #쉼
        self.tx, self.ty = self.x, 50

        if not self.distance_less_than(self.tx, self.ty, self.x, self.y, 4):
            self.move_slightly_to(self.tx, self.ty)
            return BehaviorTree.RUNNING

        if not hasattr(self, 'wait_start'):
            self.wait_start = time.time()
        elif time.time() - self.wait_start >= 3:
            del self.wait_start
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def check_wander_time(self):
        if not hasattr(self, 'wander_start_time'):
            self.wander_start_time = time.time()
            print("Wander started:", self.wander_start_time)  # 디버깅 메시지

        elapsed_time = time.time() - self.wander_start_time
        print(f"Elapsed time: {elapsed_time:.2f}")  # 경과 시간 출력

        if elapsed_time > 2:  # 2초 이상 경과 시 SUCCESS
            del self.wander_start_time
            print("Wander completed.")
            return BehaviorTree.SUCCESS  # 정확히 SUCCESS 반환

        return BehaviorTree.FAIL  # 2초가 지나지 않으면 RUNNING

    def wander_logic(self):
        # 목표 위치 설정 및 초기화
        if not hasattr(self, 'wander_initialized'):
            self.tx, self.ty = random.randint(100, 800 - 100), random.randint(100, 600 - 100)
            self.wander_start_time = None
            self.wander_initialized = True

        # 목표 위치로 이동
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 5):  # 목표 도달
            if not self.wander_start_time:  # 대기 시작 시간 기록
                self.wander_start_time = time.time()

            # 2초 대기 후 성공
            if time.time() - self.wander_start_time >= 2:
                del self.wander_initialized
                del self.wander_start_time
                return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def transition_delay(self, delay=0.1):
        if not hasattr(self, 'delay_start_time'):
            self.delay_start_time = time.time()
            return BehaviorTree.RUNNING

        if time.time() - self.delay_start_time >= delay:
            del self.delay_start_time
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # 이동
        m1 = Action('왼쪽 위로 이동', self.move_to_left_up)
        m2 = Action('오른쪽 위로 이동', self.move_to_right_up)
        m3 = Action('왼쪽 아래로 이동', self.move_to_left_down)
        m4 = Action('오른쪽 아래로 이동', self.move_to_right_down)
        m5 = Action('가운데로 이동', self.move_to_center)
        m6 = Action('가운데 위로 이동', self.move_to_upper_center)
        m7 = Action('플레이어에게 이동', self.move_to_player)

        #공격
        a7 = Action('파이어볼 발사', self.split_fire_ball)
        a8 = Action('파이어볼 발사', self.split_fire_ball)
        a9 = Action('파이어볼 발사', self.split_fire_ball)
        a10 = Action('파이어볼 발사', self.split_fire_ball)
        a11 = Action('빔', self.final_flash)
        a12 = Action('빔', self.final_flash)
        a13 = Action('빔', self.final_flash)
        a14 = Action('시계방향 발사', self.split_in_center)
        a15 = Action('불비', self.fireball_rain)
        a16 = Action('손 소환', self.fire_wave)
        a17 = Action('쉼', self.break_time)
        a18 = Action('Set random location', self.set_random_location)
        a19 = Action('Move to', self.move_to)

        # 2초 배회 체크
        c1 = check_wander_condition = Condition('2초 배회 체크', self.check_wander_time)

        # 배회
        wander1 = Action('배회1', self.wander_logic)
        wander2 = Action('배회2', self.wander_logic)
        wander3 = Action('배회1', self.wander_logic)
        wander4 = Action('배회2', self.wander_logic)
        delay1 = Action('전환 대기', self.transition_delay)
        delay2 = Action('전환 대기', self.transition_delay)
        delay3 = Action('전환 대기', self.transition_delay)
        delay4 = Action('전환 대기', self.transition_delay)
        delay5 = Action('전환 대기', self.transition_delay)
        delay6 = Action('전환 대기', self.transition_delay)
        delay7 = Action('전환 대기', self.transition_delay)
        delay8 = Action('전환 대기', self.transition_delay)

        #패턴
        pattern1 = Sequence('왼쪽 위 이동 + 발사', m1, a7, m2, a8, m3, a9, m4, a10)
        pattern2 = Sequence('가운데 위 이동 후 아래로 발사', m6, a15)
        pattern3 = Sequence('가운데 이동 + 시계방향 발사', m5, a14)
        pattern4 = Sequence('손이 올라오다', m5, a16)
        pattern5 = Sequence(
            '가운데 이동 + 발사',
            Sequence('왼쪽 위로 이동 + 빔 발사', m7, a11),
        )

        #all_pattern
        all_pattern = Sequence('랜덤 패턴 선택', pattern1, pattern2, pattern3, pattern4, pattern5)

       #===========================================================================================================

        #root = Sequence('배회 후 랜덤 패턴 실행', all_pattern, wander)
        root = Sequence('빔', pattern1,
                        delay1, wander1, delay5, pattern2,
                        delay2, wander2, delay6, pattern3,
                        delay3, wander3, delay7, pattern4,
                        delay4, wander4, delay8, pattern5)
        #root = Sequence('배회 후 랜덤 패턴 실행', m7, a11)
        # BehaviorTree에 루트 설정
        self.bt = BehaviorTree(root)

