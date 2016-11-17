from FGAme import *
from math import sqrt
from world import RainingWorld
import pygame
from pygame.locals import *
from raining_man.shot import Shot, randomize
import random
import time
import os

world = RainingWorld()
world.add_raining_world()
world.start_sound()

@listen('long-press', 'up')
def increase_drag():
    if not is_exaust:
        absolute_image_path = os.path.join(world.root, 'images/2.png')
        for shot in world.shot_list:
            shot.k = 100
    else:
        absolute_image_path = os.path.join(world.root, 'images/1.png')
        world.player.body_pygame = pygame.image.load('images/1.png')

world.render_game()
