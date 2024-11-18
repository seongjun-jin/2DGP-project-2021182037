#배경 - 0 땅 - 1, 캐릭터 - 2
world = [[], [], []]

collision_pairs = {} #{key :[[a] [b]]}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def clear():
    for layer in world:
        layer.clear()

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
            remove_collision_object(o)
            del o #메모리에서 객체 자체를 삭제
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