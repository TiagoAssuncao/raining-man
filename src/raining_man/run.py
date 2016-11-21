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


world.render_game()
