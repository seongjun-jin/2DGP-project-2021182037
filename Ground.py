from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image("8.png")

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 360, 360, 400, 150, 1000, 300)