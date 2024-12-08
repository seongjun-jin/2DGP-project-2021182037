from pico2d import *

import game_world
import game_framework
from ending_scene import ending


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.025)

def draw():
    clear_canvas()
    game_world.render()  # 모든 레이어를 렌더
    update_canvas()


def finish():
    global bgm  # bgm 변수를 전역 변수로 선언
    game_world.clear()
    if bgm:
        bgm.stop()
        del bgm


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            pass

def init():
    global bgm
    background = ending()
    game_world.add_object(background, 0)
    bgm = load_music('Pizza Time.mp3')  # 배경음악 파일 경로
    bgm.set_volume(32)  # 볼륨 설정 (0~128)
    bgm.repeat_play()  # 반복 재생
    pass

def pause():
    pass


def resume():
    pass
