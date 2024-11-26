

class sword:
    def __init__(self):
        self.x = 200
        self.y = 50
        pass
    def draw(self):

        pass
    def update(self):
        pass
    def get_bb(self):
        #하나의 튜플을 리턴
        #상태별로 바운딩 박스 바뀌게
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
        pass

    def handle_collision(self, group, other):
       pass
