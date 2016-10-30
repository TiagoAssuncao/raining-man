from FGAme import *
import pygame

class Boy:

    def __init__(self):
        self.body = world.add.aabb(shape=(30,80), pos=(400, 500), mass=500)
        self.body_pygame = pygame.image.load('images/1.png')
        self.rect = [0, 0, 60, 60]
        self.k = 1.05

    def update(self):
	    self.cont_animation += 0.1

	    if self.cont_animation < 0.75:
	        self.rect[0] = 0

	    elif self.cont_animation > 0.75:
	        self.rect[0] = 60

	    if self.cont_animation >= 1.25:
	        self.cont_animation = 0
