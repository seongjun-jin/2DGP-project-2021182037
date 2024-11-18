from pico2d import *
from State_Machine import *
import game_world
from Attack import Slash
import game_framework
from sdl2.ext.particles import Particle
#직접적인 공간수치가 아닌 프레임숫자, 시간으로 표현을 해라


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 2

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
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        player.x += player.dir * 10

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
        pass  # Jump state exits automatically when landing

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 5
        player.apply_gravity()  # Apply gravity to manage jump movement
        if not player.is_jumping:  # Return to Idle or Run after landing
            player.state_machine.change(Idle if player.dir == 0 else Run)

    @staticmethod
    def draw(player):
        # Draw the jumping sprite; adjust parameters if the jump sprite differs in dimensions
        player.image.clip_draw(80 + int(player.frame) * 20, 40, 20, 20, player.x, player.y)

class Player:
    def __init__(self):
        self.x, self.y = 400, 50
        self.MAX_hp = 5
        self.hp = self.MAX_hp
        self.frame = 0
        self.image = load_image("player.png")
        self.dir = 0
        self.attack_force = 1
        self.jump_height = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.face_dir = 1
        self.heal = False
        self.is_hit = False
        self.hit_timer = 0
        self.velocity_y = 0
        self.is_jumping = 2
        self.is_invincibility_time = 0
        self.is_invincibility = False
        self.is_attacking = False
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, z_down:Idle, UP_down:Idle},
            Run: {right_up: Idle, left_up: Idle, right_down: Idle, left_down: Idle, z_down:Run, UP_down:Run}
        })

    def handle_event(self, event):
        self.state_machine.add_event(['INPUT', event])

    def update(self):
        self.state_machine.update()
        if self.is_jumping >= 0:
            self.apply_gravity()
        if self.is_hit:  # 일정 시간 후 다시 충돌 가능
            self.hit_timer -= game_framework.frame_time
            if self.hit_timer <= 0:
                self.is_hit = False
        if self.heal:
            while self.hp < self.MAX_hp:
                self.hp += 1
        self.heal = False

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def Jump(self):
        if self.is_jumping > 0:
            self.is_jumping -= 1
            self.velocity_y = 15

    def apply_gravity(self):
        self.y += self.velocity_y
        self.velocity_y -= 2

        if self.y <= 50:
            self.y = 50
            self.velocity_y = 0
            self.is_jumping = 5

    def Attack(self):
            slash = Slash(self.x, self.y, self.face_dir)
            game_world.add_object(slash, 1)
            slash.attacker = self
            game_world.add_collision_pair('boss:attack', None, slash)


    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8
        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'boss:player' and not self.is_hit:
            self.is_hit = True
            self.hp -= 1
            self.hit_timer = 1
        if group == 'player:bonfire':
            self.heal = True
        pass

