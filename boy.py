from FGAme import *

class Boy:

    def __init__(self):
        self.body = world.add.aabb(shape=(30,80), pos=(400, 500), mass=500)
        self.k = 1.05

    def update(self):
        pass
