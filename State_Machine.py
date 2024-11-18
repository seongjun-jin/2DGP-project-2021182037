#event
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_z, SDLK_UP, SDLK_DOWN


def space_down(e):
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and
            e[1].key == SDLK_SPACE)

def start_event(e):
    return e[0] == 'START'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def UP_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def DOWN_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def time_out(e):
    return e[0] == 'TIME_OUT'

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z

#상태머신을 처리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o #boy self가 전달이됨 self.o = 상태머신과 연결된 캐릭터 객체
        self.event_que = [] #발생하는 이벤트 담는 곳
        pass

    def update(self):
        # 현재 상태 업데이트
        self.cur_state.do(self.o)

        # 이벤트 발생 시 상태 전이
        if self.event_que:
            e = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):

                    self.cur_state.exit(self.o, e)
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    return

    def add_event(self, e):
        self.event_que.append(e)
        print(f'   DEBUG: new event{e}')

    def start(self, start_state):
        #현재상태를 시작상태로 만들어줌
        self.cur_state = start_state
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass