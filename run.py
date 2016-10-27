from FGAme import *
from math import sqrt
from boy import *
from shot import Shot
import random
import time

world.add.margin(200, -500)
world.gravity = (0, 10)
player = Boy()
player.body.gravity = (0, 0)
gravity_x, gravity_y = player.body.gravity

shot_list = []
shot = Shot() # INITIAL SHOT
shot_list.append(shot)

def randomize():
	for i in range(random.randint(1, 2)):
		shot = Shot()
		randomizer = random.randint(-100, 100)
		shot.x = randomizer + random.randint(250, 350)
		shot.y = shot.y + random.randint(-70, -50) # TO NOT GET TOGETHER
		shot_list.append(shot)

@listen('long-press', 'up')
def increase_drag():
	for shot in shot_list:
		shot.k = 1.05

@listen('key-up', 'up')
def decrease_drag():
	for shot in shot_list:
		shot.k = 0.1

@listen('key-down', 'x')
def exit_game():
	exit()


timer = 0 # GAME TIMER
@listen ('frame-enter')
def update():
	global timer
	if timer >= 400: # TIME TO SPAWN
		timer = 0
		randomize()

	for shot in shot_list:
		shot.update()

		if shot.pos[1] > 600:
			print ("REMOVING OBJECT")
			shot_list.remove(shot)
			world.remove(shot)

	# END GAME
	if player.body.vel[1] > 0:
		print("GAME OVER")
		exit()

	# TIMER INCREASING DEPENDS ON K VALUE
	if (shot_list[0].k) == 0.1:
		timer += 1
	else: # SLOW DOWN THE TIME
		timer += 0.5

run()
