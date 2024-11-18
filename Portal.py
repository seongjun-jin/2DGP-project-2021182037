from pico2d import load_image, load_font, draw_rectangle
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class portal:
    def __init__(self):
        self.x, self.y = 100, 70
        self.image = load_image("portal.png")
        self.font = load_font('ENCR10B.TTF', 16)
        self.is_guide = False
        if self.image is None:
            print("이미지를 로드하지 못했습니다. 'portal.png' 경로를 확인하세요.")
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        self.is_guide = False
        print(f"현재 프레임: {self.frame}")

    def draw(self):
        if self.image:
            if self.is_guide:
                self.image.clip_draw(0 + int(self.frame) * 63, 85, 63, 85, self.x, self.y, 50, 50)
                self.font.draw(self.x - 10, self.y + 50, f'PRESS DOWN key', (255, 255, 0))
            else:
                self.image.clip_draw(0 + int(self.frame) * 63, 85, 63, 85, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 20, self.y -30, self.x + 20, self.y + 30
        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'player:portal':
            self.is_guide = True

            pass