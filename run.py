from FGAme import *
from math import sqrt
from boy import *
from shot import Shot
import random
import time

world.add.margin(200, -500)
world.gravity = (0, 30)
player = Boy()
player.body.gravity = (0, 0)
gravity_x, gravity_y = player.body.gravity

shot_list = []
shot = Shot() # INITIAL SHOT
shot_list.append(shot)
count = 0

def randomize():
	for i in range(random.randint(1, 2)):
		shot = Shot()
		global count
		count = count + 1
		randomizer = random.randint(-100, 100)
		shot.x = randomizer + random.randint(300, 500)
		shot.y = shot.y + random.randint(-70, -50) # TO NOT GET TOGETHER
		shot_list.append(shot)
		shot.vel = (0, 10 + 10*count)

@listen('long-press', 'up')
def increase_drag():
	for shot in shot_list:
		shot.k = 100	

@listen('long-press', 'left', dx=-2)
@listen('long-press', 'right', dx=2)
def move_p1(dx):
        player.body.move(dx, 0)

@listen('key-up', 'up')
def decrease_drag():
	for shot in shot_list:
		shot.k = 0.05

@listen('key-down', 'x')
def exit_game():
	exit()


timer = 0 # GAME TIMER
auxiliar_k = 0
@listen ('frame-enter')
def update():
	global timer
	global auxiliar_k
	if timer >= 100: # TIME TO SPAWN
		timer = 0
		randomize()

	for shot in shot_list:
		shot.update()

		if shot.pos[1] > 600:
			shot_list.remove(shot)
			world.remove(shot)

	# END GAME
	if player.body.vel[1] > 0:
		print("GAME OVER")
		exit()

	# TIMER INCREASING DEPENDS ON K VALUE
	if not shot_list:
		timer += 1
	elif (shot_list[0].k) == 0.1:
		timer += 1
	else: # SLOW DOWN THE TIME
		timer += 0.5

run()
