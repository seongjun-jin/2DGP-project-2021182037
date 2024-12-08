from pico2d import *
from State_Machine import *
import game_world
from Attack import Slash
import game_framework
import server
import bossroom1_mode
#직접적인 공간수치가 아닌 프레임숫자, 시간으로 표현을 해라

update_count = 0
draw_count = 0


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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

class player_hp:
    def __init__(self, player):
        self.player = player
        self.x, self.y = 25, 25  # 체력 바 위치 (왼쪽 상단)
        self.heart_width = 60  # 하트 하나의 너비
        self.image = load_image("player_hp.png")  # 하트 이미지를 로드

    def update(self):
        pass

    def draw(self):
        for i in range(self.player.hp):  # 현재 체력만큼만 하트를 그립니다.
            x_pos = self.x + i * self.heart_width  # 각 하트의 위치 계산
            self.image.clip_draw(0, 0, self.heart_width, 50, x_pos, self.y, self.heart_width, 50)

class Idle:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.dir = -1
            player.face_dir = -1
        elif left_down(e) or right_up(e):
            player.dir = 1
            player.face_dir = 1

    @staticmethod
    def exit(player, e):
        if UP_down(e):
            player.Jump()
        elif z_down(e):
            player.Attack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 20, 40, 20, 20, player.x, player.y,20,20)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 20, 40, 20, 20, 0,'h',player.x, player.y,20,20)

class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.dir = 1
            player.face_dir = 1
        elif left_down(e) or right_up(e):
            player.dir = -1
            player.face_dir = -1

        player.frame = 0
        print(f"Entering Run State with dir = {player.dir}")  # 디버그 메시지

    @staticmethod
    def exit(player, e):
       if UP_down(e):
           player.Jump()
       elif z_down(e):
           player.Attack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        print(f"Player frame: {player.frame}")

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 20, 0, 20, 20, player.x, player.y, 20, 20)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 20, 0, 20, 20, 0, 'h', player.x, player.y, 20, 20)

class Jump:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        print("Entering Jump State")

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 5
        player.apply_gravity()
        if not player.is_jumping:
            player.state_machine.change(Idle if player.dir == 0 else Run)

    @staticmethod
    def draw(player):
        player.image.clip_draw(80 + int(player.frame) * 20, 40, 20, 20, player.x, player.y)

class Player:
    def __init__(self):
        self.x = 400
        self.y = 50
        self.MAX_hp = 5
        self.hp = self.MAX_hp
        self.hp_bar = player_hp(self)
        self.frame = 0
        self.image = load_image("player(1).png")
        self.dir = 0
        self.attack_force = 1
        self.jump_height = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.death_font = load_font('강원교육튼튼.TTF', 50)
        self.face_dir = 1
        self.heal = False
        self.is_hit = False
        self.hit_timer = 0
        self.velocity_y = 0
        self.is_jumping = 2
        self.is_attacking = False
        self.is_dead = False
        self.is_falling = False
        self.current_portal = None
        self.item_select = False
        self.current_item = None
        self.select_item = None
        self.select_item_image = None
        self.enter_bossroom = False
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, z_down: Idle, UP_down: Idle},
            Run: {right_up: Idle, left_up: Idle, right_down: Idle, left_down: Idle, z_down: Run, UP_down: Run}
        })

    def handle_event(self, event):
        if not self.is_dead:
            self.state_machine.add_event(['INPUT', event])

        if self.current_portal and event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            self.enter_portal(self.current_portal)

        if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if self.current_item:  # 현재 충돌 중인 아이템이 있을 때
                self.current_item.apply_effect(self)  # 아이템 획득

    def update(self):
        if self.is_dead:
            if self.is_falling:
                self.y -= 2
                if self.y <= 50:
                    self.y = 50
                    self.is_falling = False
            return
        self.state_machine.update()
        if self.is_jumping >= 0:
            self.apply_gravity()
        if self.is_hit:
            self.hit_timer -= game_framework.frame_time
            if self.hit_timer <= 0:
                self.is_hit = False
        if self.heal:
            while self.hp < self.MAX_hp:
                self.hp += 1
        self.heal = False
        self.current_portal = None
        self.item_select = None

        if self.hp <= 0 and not self.is_dead:
            self.die()
        self.x = clamp(25, self.x, 775)
        self.y = clamp(50, self.y, 500)

    def draw(self):
        if self.is_dead:
            self.image.clip_composite_draw(int(self.frame) * 20, 0, 20, 20, math.radians(90), '', self.x, self.y, 20, 20)
            self.death_font.draw(300, 300, "YOU DIED", (255, 0, 0))
        else:
            self.state_machine.draw()
            self.font.draw(self.x - 10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        if self.select_item_image:
            self.select_item_image.draw(50, 550, 40, 40)
        self.hp_bar.draw()


    def Jump(self):
        if not self.is_dead and self.is_jumping > 0:
            self.is_jumping -= 1
            self.velocity_y = 15

    def apply_gravity(self):
        if self.is_dead:
            return  # No gravity effect if dead
        self.y += self.velocity_y
        self.velocity_y -= 2

        if self.y <= 50:
            self.y = 50
            self.velocity_y = 0
            self.is_jumping = 5

    def Attack(self):
        if not self.is_dead:
            slash = Slash(self.x, self.y, self.face_dir)
            game_world.add_object(slash, 1)
            slash.attacker = self
            game_world.add_collision_pair('boss:attack', None, slash)

    def die(self):
        self.is_dead = True
        self.is_falling = True
        self.dir = 0
        self.velocity_y = 0
        print("Player has died!")

    def get_bb(self):
        if self.is_dead:
            return 0, 0, 0, 0  # No collision box when dead
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def handle_collision(self, group, other):
        if self.is_dead:
            return
        if group == 'boss:player' and not self.is_hit:
            self.is_hit = True
            self.hp -= 1
            self.hit_timer = 1
        if group == 'player:bonfire':
            self.heal = True
        if group == 'player:portal':
            self.current_portal = other
        if group == 'player:item':
            self.current_item = other
            pass
        if group == 'player:attack' and not self.is_hit:
            self.is_hit = True
            self.hp -= 1
            self.hit_timer = 1

    def enter_portal(self, portal):
        """포탈을 통해 다른 맵으로 이동"""
        if portal.target_map:
            print(f"Entering portal to {portal.target_map}!")
            # 플레이어 위치 갱신
            self.x = portal.target_x
            self.y = portal.target_y
            portal.target_map.player = self
            game_framework.change_mode(portal.target_map)
            server.players_map = portal.target_map

    def Acquire_Item(self, item):
        print(f"Player acquired item: {type(item).__name__}")
        item.apply_effect(self)  # 아이템 효과를 플레이어에 적용
        game_world.remove_object(item)  # 게임 월드에서 아이템 제거
        self.select_item = item
        self.select_item_image = item.image





