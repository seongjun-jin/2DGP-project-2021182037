from pico2d import *

class B1_BG:
    def __init__(self):
        self.image = load_image("bg.png")
        if self.image is None:
            print("Image failed to load")

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 2300, 1300, 400, 300, 1500, 1000)