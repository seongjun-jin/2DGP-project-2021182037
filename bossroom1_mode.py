from pico2d import *

import game_world
import game_framework
from Ground import Ground
from bossroom1_bg import B1_BG
from bonfire import bonfire
from Portal import portal
from Boss1 import boss
import Player
import title_mode

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.025)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass


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
    global player
    global boss
    if player is None:  # 이전 모드에서 전달된 객체가 없으면 새로 생성
        print("Player object not passed, creating a new one.")
        player = Player.Player()  # Player 모듈에서 객체 생성
    else:
        print("Player object received from previous mode.")
    game_world.add_object(player, 2)

        # 플레이어를 게임 월드에 추가
    game_world.add_object(player, 2)

    boss = boss()
    game_world.add_object(boss, 2)

    ground = Ground()
    game_world.add_object(ground, 1)

    background = B1_BG()
    game_world.add_object(background, 0)

    game_world.add_collision_pair('boss:player', player, None)
    game_world.add_collision_pair('boss:player', None, boss)

    game_world.add_collision_pair('boss:attack', boss, None)

def pause():
    pass

def resume():
    pass