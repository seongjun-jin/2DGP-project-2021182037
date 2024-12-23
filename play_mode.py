#from Lecture14_Game_Framework import title_mode, item_mode
from pico2d import *

import game_world
import game_framework
from Player import Player
from Ground import Ground
from Background import BG
import bossroom1_mode
from bonfire import bonfire
from Portal import portal
from Boss1 import boss
import title_mode
import server
from sword import Sword
from heart import Heart

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.025)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    global image, bgm

    # 배경음악 정리
    if bgm:
        bgm.stop()
        del bgm


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
             game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            server.player.handle_event(event)


def init():
    global player
    global portal
    global bonfire
    global sword
    global heart
    global boss
    global bgm
    #boss = boss()
    #game_world.add_object(boss, 2)

    server.player = Player()
    game_world.add_object(server.player, 2)

    ground = Ground()
    game_world.add_object(ground, 1)

    portal = portal(100, 70, 50, 50, bossroom1_mode, 400, 50)
    game_world.add_object(portal, 1)


    #bonfire = bonfire()
    #game_world.add_object(bonfire, 1)

    background = BG()
    game_world.add_object(background, 0)

    sword = Sword()
    game_world.add_object(sword, 1)

    heart = Heart()
    game_world.add_object(heart, 1)

    game_world.add_collision_pair('player:item', server.player, None)
    game_world.add_collision_pair('player:item', None, sword)
    game_world.add_collision_pair('player:item', None, heart)

    game_world.add_collision_pair('player:attack', server.player, None)

    game_world.add_collision_pair('player:portal', server.player, None)
    game_world.add_collision_pair('player:portal', None, portal)

    #game_world.add_collision_pair('player:bonfire', server.player, None)
    #game_world.add_collision_pair('player:bonfire', None, bonfire)
    bgm = load_music('play.mp3')  # 배경음악 파일 경로
    bgm.set_volume(32)  # 볼륨 설정 (0~128)
    bgm.repeat_play()  # 반복 재생

def pause():
    pass

def resume():
    pass

