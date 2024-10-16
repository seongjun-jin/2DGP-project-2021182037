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

class BG:
    def __init__(self):
        self.image = load_image("bg.png")
        if self.image is None:
            print("Image failed to load")

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)

class Player:
    def __init__(self):
        self.x, self.y = 400, 30
        self.frame = 0
        self.image = load_image("player.png")

    def handle_event(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 20, 40, 20, 20, self.x, self.y)

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
    global player
    running = True
    world = []

    player = Player()
    bg = BG()
    chara = Character()

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