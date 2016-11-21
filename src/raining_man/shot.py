from FGAme import *
import random
import os
import pygame


def randomize(shot_list, count, world_vel):
    for i in range(random.randint(1, 3)):
        shot = Shot()
        count = count + 1
        randomizer = random.randint(-100, 100)
        shot.x = randomizer + random.randint(270, 420)
        shot.y = shot.y + random.randint(-80, -50) # TO NOT GET TOGETHER
        shot_list.append(shot)
        print(world_vel)
        shot.vel = world_vel

class Shot(AABB):

    def __init__(self, pos=(400, 650)):
        super().__init__(shape=(100, 50),mass=10000, pos=pos, vel=(0, 100), 
                         color='brown')
        self.body = world.add(self)

        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, 'images/pedra1.png')
        self.body_pygame = pygame.image.load(absolute_image_path)
        self.k = 1.05

    def update(self):
        x, y = self.vel
        drag = abs(self.k * (y ** 2))
        a = (self.mass * self.gravity[1] - drag) / self.mass
        speed_x, speed_y = self.vel
        speed_y += a * 1/60
        pos_x, pos_y = self.pos
        pos_y -= speed_y * 1/60
        self.vel = (speed_x, speed_y)
        self.pos = pos_x, pos_y
