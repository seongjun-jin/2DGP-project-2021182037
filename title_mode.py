import play_mode
from pico2d import clear_canvas, update_canvas, load_image, get_events, load_music
from sdl2 import SDLK_ESCAPE, SDL_QUIT, SDL_KEYDOWN, SDLK_SPACE
import game_framework

def init():
    global image, bgm
    image = load_image('title3.png')

    bgm = load_music('Main Menu.mp3')  # 배경음악 파일 경로
    bgm.set_volume(32)  # 볼륨 설정 (0~128)
    bgm.repeat_play()  # 반복 재생

def finish():
    global image, bgm
    del image

    # 배경음악 정리
    if bgm:
        bgm.stop()
        del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.type == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1717, 890, 400, 300, 800, 600)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass