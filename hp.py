from pico2d import load_image


class hp_bar:
    def __init__(self, boss):
        self.x, self.y = 400, 580  # HP 바 위치
        self.image = load_image("hp_bar.png")
        self.boss = boss  # 보스 객체를 저장
        self.hp_width = 364  # HP 바의 전체 너비 (이미지의 클립 영역)

    def update(self, current_hp, max_hp):
        """보스의 HP를 기반으로 비율 업데이트"""
        self.hp_ratio = current_hp / max_hp if max_hp > 0 else 0
        self.hp_width = 364 * self.hp_ratio  # HP 바 길이 비율로 조정

    def draw(self):
        """HP 바를 화면에 그리기"""
        # HP 바의 현재 길이를 그리기
        self.image.clip_draw(
            0, 0, int(self.hp_width), 44,  # 클립 영역 조정 (너비만 변경)
            self.x, self.y
        )

