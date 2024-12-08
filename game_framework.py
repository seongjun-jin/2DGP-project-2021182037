import time
import game_world
from game_world import world
from pico2d import draw_rectangle

running = None
stack = None
screen_offset_x = 0
screen_offset_y = 0

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 프레임 타임 관련 변수
frame_time = 0.0
target_fps = 60  # 목표 FPS
fixed_frame_time = 1.0 / target_fps  # 고정 프레임 타임 (선택)

screen_color = (0, 0, 0)  # 기본 화면 색상 (검정색)

def fill_rectangle(x1, y1, x2, y2, color):
    r, g, b = color
    #set_color(r, g, b)
    draw_rectangle(x1, y1, x2, y2)

def clear_canvas():
    global screen_color
    #fill_rectangle(0, 0, get_canvas_width(), get_canvas_height(), screen_color)

def get_frame_time():
    """현재 프레임 타임을 반환"""
    global frame_time
    return frame_time

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    game_world.clear_all()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()

    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.init()

    current_time = time.time()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        # 프레임 타임 계산 및 FPS 제한
        frame_time = time.time() - current_time
        if frame_time < fixed_frame_time:
            time.sleep(fixed_frame_time - frame_time)  # FPS 제한
            frame_time = fixed_frame_time  # 강제 고정 프레임 타임
        current_time += frame_time

        # FPS 디버깅
        print(f"FPS: {1.0 / frame_time:.2f}, Frame Time: {frame_time:.6f}")


    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()
