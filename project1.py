from pico2d import *
import random
import os

class Character:
    def __init__(self):
        self.x, self.y = 400,300
        self.frame = 0
        self.action = 3
        self.image = load_image("run_animation.png")

    def handle_event(self):
        pass

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)

class BG:
    def __init__(self):
        self.image = load_image("run_animation.png")

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def reset_world():
    global running
    global world
    global chara
    global bg

    running = True

    world = []

    bg = BG()
    chara = Character()

    world.append(bg)
    world.append(chara)

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_world()
    pass

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