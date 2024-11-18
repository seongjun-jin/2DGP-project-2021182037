import game_framework
import play_mode
import title_mode as start_mode
from pico2d import open_canvas, close_canvas

open_canvas()
# game loop
game_framework.run(start_mode)
close_canvas()