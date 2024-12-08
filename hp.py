from pico2d import load_image
from Boss1 import boss

class hp_bar:
    def __init__(self, boss):
        self.hp_ratio = None
        self.boss = boss
        self.hp_image = load_image("hp.png")
        self.back_image = load_image("hp_bar.png")
        self.hp_width = 588  # 초기 너비 설정
        self.x, self.y = 400, 580  # HP 바 위치

    def update(self, hp, max_hp):
        self.hp_ratio = hp / max_hp if max_hp > 0 else 0
        self.hp_width = 588 * self.hp_ratio  # HP 비율에 따라 너비 조정
        print(f"HP Bar Updated: {self.hp_ratio * 100:.1f}%")

    def draw(self):
        # Draw the HP background
        self.back_image.clip_draw(0, 0, 616, 83, self.x, self.y - 40)

        # Draw the HP bar according to current HP
        self.hp_image.clip_draw(0, 0, int(self.hp_width), 30, self.x - (588 - self.hp_width) / 2, self.y - 40)



