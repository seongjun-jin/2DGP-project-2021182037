from pico2d import *

class Player:
    def __init__(self):
        self.x, self.y = 400, 80
        self.frame = 0
        self.image = load_image("player.png")
        self.dir = 1
        self.run = False
        self.idle = False

    def handle_event(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2

    def draw(self):
        if self.idle:
            self.image.clip_draw(self.frame * 20, 40, 20, 20, self.x, self.y)
        elif self.run:
            self.image.clip_draw(self.frame * 20, 0, 20, 20, self.x, self.y)