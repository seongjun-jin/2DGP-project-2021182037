#from Lecture14_Game_Framework import title_mode, item_mode
from pico2d import *

import game_world
import game_framework
from Player import Player
from Ground import Ground
from Background import BG
from bonfire import bonfire
from Portal import portal
from Boss1 import boss
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
    global portal
    global bonfire

    boss = boss()
    game_world.add_object(boss, 2)

    player = Player()
    game_world.add_object(player, 2)

    ground = Ground()
    game_world.add_object(ground, 1)

    portal = portal()
    game_world.add_object(portal, 1)

    bonfire = bonfire()
    game_world.add_object(bonfire, 1)

    background = BG()
    game_world.add_object(background, 0)

    game_world.add_collision_pair('boss:player', player, None)
    game_world.add_collision_pair('boss:player', None, boss)

    game_world.add_collision_pair('player:portal', player, None)
    game_world.add_collision_pair('player:portal', None, portal)

    game_world.add_collision_pair('player:bonfire', player, None)
    game_world.add_collision_pair('player:bonfire', None, bonfire)

    game_world.add_collision_pair('boss:attack', boss, None)



def pause():
    pass

def resume():
    pass

