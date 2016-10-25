from FGAme import *

class Shot(AABB):

    def __init__(self, pos=(200, 0)):
        super().__init__(shape=(100, 50),mass=100, pos=pos, vel=(0, 0))
        self.k = 0.1

    def update(self):
        x, y = self.vel
        drag = abs(self.k * (y ** 2))
        a = (self.mass * self.gravity[1] - drag) / self.mass
        print(a)
        speed_x, speed_y = self.vel
        speed_y += a * 1/60
        pos_x, pos_y = self.pos
        pos_y -= speed_y * 1/60
        self.vel = (speed_x, speed_y)

        print(self.vel, self.pos)
        if(self.pos[1] > 700 or self.pos[1] < -50):
            self.shape = (400, 50)
            self.pos = (200, 0)
