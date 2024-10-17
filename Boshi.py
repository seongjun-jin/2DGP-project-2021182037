from pico2d import *

class Character:
    def __init__(self):
        self.x, self.y = 400,300
        self.frame = 0
        self.image = load_image("1.png")
        if self.image is None:
            print("Image failed to load")

    def handle_event(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 75, 2700, 75, 105, self.x, self.y)