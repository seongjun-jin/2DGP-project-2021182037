from pico2d import *
from Boshi import Character
from Background import BG
from Ground import Ground
#from Player import Player
import random

class Player:
    def __init__(self):
        self.x, self.y = 400, 80
        self.frame = 0
        self.image = load_image("player.png")
        self.dir = 0
        self.run = False
        self.idle = True
        self.speed = 5

    def handle_event(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2
        self.x -= self.dir * self.speed

    def draw(self):
        if self.idle:
            self.image.clip_draw(self.frame * 20, 40, 20, 20, self.x, self.y)
        elif self.run:
            self.image.clip_draw(self.frame * 20, 0, 20, 20, self.x, self.y)

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            player.idle = False
            player.run = True
            player.dir += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            player.idle = False
            player.run = True
            player.dir -= 1
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            player.idle = True
            player.run = False
            player.dir -= 1
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            player.idle = True
            player.run = False
            player.dir += 1



def reset_world():
    global running
    global world
    global chara
    global bg
    global player
    global ground

    running = True
    world = []

    player = Player()
    bg = BG()
    chara = Character()
    ground = Ground()

    world.append(ground)
    world.append(bg)
    world.append(chara)
    world.append(player)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()


reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()