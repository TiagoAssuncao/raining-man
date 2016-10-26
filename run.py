from FGAme import *
from math import sqrt
from boy import *
from shot import Shot

world.add.margin(200, -500)
world.gravity = (0, 10)
player = Boy()
player.body.gravity = (0, 0)
gravity_x, gravity_y = player.body.gravity
shot = Shot()
world.add(shot)

@listen('long-press', 'up')
def increase_drag():
    shot.k = 10

@listen('key-up', 'up')
def decrease_drag():
    shot.k = 1.05


@listen('key-down', 'x')
def exit_game():
    exit()

def update():
    shot.update()

#world.add(player)


run()
