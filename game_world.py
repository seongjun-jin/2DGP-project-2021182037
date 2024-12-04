import time
import random

#배경 - 0 땅 - 1, 캐릭터 - 2
world = [[], [], [], []]

collision_pairs = {} #{key :[[a] [b]]}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)



# 흔들림 오프셋
screen_shake_intensity = 0  # 흔들림 강도
screen_shake_duration = 0  # 흔들림 지속 시간
shake_start_time = 0       # 흔들림 시작 시간

def start_screen_shake(intensity, duration):
    """화면 흔들림 시작"""
    global screen_shake_intensity, screen_shake_duration, shake_start_time
    screen_shake_intensity = intensity
    screen_shake_duration = duration
    shake_start_time = time.time()

def apply_screen_shake():
    """현재 흔들림 오프셋 반환"""
    global screen_shake_intensity, screen_shake_duration, shake_start_time

    if screen_shake_duration > 0:
        elapsed_time = time.time() - shake_start_time
        if elapsed_time >= screen_shake_duration:
            # 흔들림 종료
            screen_shake_intensity = 0
            screen_shake_duration = 0
            return 0, 0
        else:
            # 흔들림 오프셋 생성
            offset_x = random.uniform(-screen_shake_intensity, screen_shake_intensity)
            offset_y = random.uniform(-screen_shake_intensity, screen_shake_intensity)
            return offset_x, offset_y
    return 0, 0

def draw_with_shake():
    """모든 오브젝트에 흔들림 효과 적용하여 그리기"""
    offset_x, offset_y = apply_screen_shake()  # 흔들림 오프셋 계산

    for layer in world:
        for obj in layer:
            obj.draw(offset_x, offset_y)  # 흔들림 오프셋 적용


def clear():
    for layer in world:
        layer.clear()

def clear_collisions():
    """맵 전체의 충돌 페어를 초기화합니다."""
    collision_pairs.clear()

def clear_all():
    clear()
    clear_collisions()

def add_object(o, depth):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)  # 충돌 페어에서 제거
            del o  # 메모리에서 객체 삭제
            return
    raise ValueError('Cannot delete non existing object')



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def handle_collisions():
    #게임월드에 등록된 충돌정보를 바탕으로 실제 충돌검사를 수행.
    for group, pairs in collision_pairs.items():
        for a in pairs[0]: # a리스트에서 하나 뽑고
            for b in pairs[1]:# b리스트에서 하나 뽑음
                if collide(a,b):
                    print(f'{group} collide')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)