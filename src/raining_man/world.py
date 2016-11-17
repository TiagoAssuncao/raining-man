"""
NOT USED YET.
"""

from FGAme import *
from boy import Boy
from shot import Shot
import pygame
from pygame.locals import *

class RainingWorld(World):
    def __init__(self):
        super().__init__()
        self.base_k = 1.05
        self.recover_interval = 150
        self.time_to_exaust = 200
        self.spawn_time = 130
        self.screen_end = -10
        self.shot_list = []
        self.count = 0
        self.points = 0
        self.is_exaust = False

    def add_raining_world(self):
        """TODO: Docstring for add_raining_world.
        :returns: nothing

        create the objects to the rainging world

        """

        self.add.margin(200, -500)
        self.gravity = (0, 30)

        self.player = Boy()
        self.player.body.gravity = (0, 0)
        shot = Shot() # INITIAL SHOT
        self.shot_list.append(shot)

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
