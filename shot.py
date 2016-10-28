from FGAme import *
import random

class Shot(AABB):

    def __init__(self, pos=(200, -10)):
        super().__init__(shape=(100, 50),mass=100, pos=pos, vel=(0, 50))
        self.body = world.add(self)
        self.k = 0.05

    def update(self):
        x, y = self.vel
        drag = abs(self.k * (y ** 2))
        a = (self.mass * self.gravity[1] - drag) / self.mass
        speed_x, speed_y = self.vel
        speed_y += a * 1/60
        pos_x, pos_y = self.pos
        pos_y -= speed_y * 1/60
        self.vel = (speed_x, speed_y)

        #print(self.vel, self.pos)
