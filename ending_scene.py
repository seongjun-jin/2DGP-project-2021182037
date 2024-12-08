from pico2d import *

class ending:
    def __init__(self):
        self.image = load_image("ending.png")
        if self.image is None:
            print("Image failed to load")

    def update(self):
        pass

    def draw(self):
        # 원래 이미지 크기
        original_width = 900
        original_height = 696

        # 화면 크기
        screen_width = 800
        screen_height = 600

        # 비율 계산
        width_ratio = screen_width / original_width
        height_ratio = screen_height / original_height
        scale_ratio = min(width_ratio, height_ratio)  # 작은 비율에 맞춰서 스케일 조정

        # 조정된 크기
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)

        # 화면 중앙 좌표
        center_x = screen_width // 2
        center_y = screen_height // 2

        # 검정색 배경 설정
        clear_canvas()

        # 엔딩 이미지 출력
        self.image.draw(center_x, center_y, new_width, new_height)
