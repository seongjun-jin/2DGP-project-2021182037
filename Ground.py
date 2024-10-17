from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image("ground.png")
        if self.image is None:
            print("Image failed to load")

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 200)
