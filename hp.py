from pico2d import load_image
from Boss1 import boss

class hp_bar:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image("hp_bar.png")
        self.hp_width = 673  # 초기 너비 설정
        self.x, self.y = 400, 580  # HP 바 위치

    def update(self, current_hp, max_hp):
        self.hp_ratio = current_hp / max_hp if max_hp > 0 else 0
        self.hp_width = 673 * self.hp_ratio  # HP 비율에 따라 너비 조정
        print(f"HP Bar Updated: {self.hp_ratio * 100:.1f}%")

    def draw(self):
        print("Drawing HP Bar...")
        self.image.clip_draw(0, 0, int(self.hp_width), 144, self.x, self.y - 40 )



