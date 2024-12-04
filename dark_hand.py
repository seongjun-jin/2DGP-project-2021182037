import game_world
import game_framework
from pico2d import load_image, draw_rectangle


class hand:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.opacity = 1.0  # 손의 투명도 (1.0 = 불투명, 0.0 = 완전 투명)
        self.state = "rising"  # 상태: rising (올라감) -> holding (머무름) -> fading (사라짐)
        self.hold_timer = 0.0  # 머무르는 시간
        self.rise_speed = 70  # y좌표가 올라가는 속도
        self.fade_speed = 1.5  # 투명도가 줄어드는 속도
        self.image = load_image('dark_hand.png')

    def update(self):
        if self.state == "rising":  # 올라가는 상태
            self.y += self.rise_speed * game_framework.frame_time
            if self.y >= 50:  # 목표 위치에 도달
                self.y = 50
                self.state = "holding"
                self.hold_timer = 0.1  # 0.5초 동안 머무름

        elif self.state == "holding":  # 머무르는 상태
            self.hold_timer -= game_framework.frame_time
            if self.hold_timer <= 0:
                self.state = "fading"

        elif self.state == "fading":  # 사라지는 상태
            self.opacity -= self.fade_speed * game_framework.frame_time
            if self.opacity <= 0:
                game_world.remove_object(self)  # 투명도가 0이 되면 제거

    def draw(self):
        if self.opacity > 0:

            # 이미지의 투명도 조절하여 그리기
            self.image.opacify(self.opacity)  # `opacify`는 이미지 투명도를 설정
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 100, self.y - 33, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'player:attack':
            pass