from pico2d import *

import server
import game_world
import game_framework
from Ground import Ground
from bossroom1_bg import B1_BG
from bonfire import bonfire
from Portal import portal
from Boss1 import boss
import Player
import title_mode
from hp import hp_bar

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def update():
    print("Updating game world...")
    game_world.update()

    if boss_instance:
        print(f"Updating Boss: {boss_instance}")
        boss_instance.update()

    game_world.handle_collisions()
    delay(0.025)

def draw():
    clear_canvas()
    game_world.render()  # 모든 레이어를 렌더링
    if boss_instance and boss_instance.hp_bar:
        boss_instance.hp_bar.draw()  # HP 바를 별도로 렌더링
    update_canvas()



def finish():
    game_world.clear()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)


def init():
    global player, boss_instance, hp

    # 플레이어 객체 초기화
    if player is None:  # 이전 모드에서 전달된 객체가 없으면 새로 생성
        print("Player object not passed, creating a new one.")
        player = Player.Player()
    else:
        print("Player object received from previous mode.")
    game_world.add_object(player, 2)  # 플레이어를 게임 월드에 추가

    # 보스 객체 및 HP 바 초기화
    boss_instance = boss()  # 보스 객체 생성
    print(f"Boss instance created: {boss_instance}")  # 보스 생성 확인
    game_world.add_object(boss_instance, 2)  # 보스를 게임 월드에 추가

    hp = hp_bar(boss_instance)  # 보스 객체를 참조하는 HP 바 생성
    boss_instance.hp_bar = hp  # 보스가 HP 바를 참조하도록 설정
    game_world.add_object(hp, 2)  # HP 바를 게임 월드에 추가

    # 보스 객체가 올바르게 추가되었는지 확인
    for obj in game_world.world[2]:
        print(f"Object in layer 2: {obj}, Type: {type(obj)}")

    # 환경 객체 추가
    ground = Ground()
    game_world.add_object(ground, 1)

    background = B1_BG()
    game_world.add_object(background, 0)

    # 충돌 페어 설정
    game_world.add_collision_pair('boss:player',player, boss_instance)
    game_world.add_collision_pair('boss:attack', boss_instance, None)
    game_world.add_collision_pair('player:attack', player, None)

def pause():
    pass


def resume():
    pass
