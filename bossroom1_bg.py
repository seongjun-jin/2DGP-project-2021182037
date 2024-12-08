from pico2d import *

class B1_BG:
    def __init__(self):
        self.image = load_image("bg.png")
        if self.image is None:
            print("Image failed to load")

    def update(self):
        pass

    def draw(self):
        # 이미지 원본 크기
        original_width = 315
        original_height = 250

        # 창 크기
        screen_width = 800
        screen_height = 600

        # 비율 계산
        scale_x = screen_width / original_width
        scale_y = screen_height / original_height
        scale = max(scale_x, scale_y)  # 창을 완전히 덮으려면 최대값 사용

        # 이미지 크기 계산
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # 화면 중심에 이미지 배치
        center_x = screen_width // 2
        center_y = screen_height // 2

        # 그리기
        self.image.clip_draw(0, 0, original_width, original_height,
                             center_x, center_y, new_width, new_height)
