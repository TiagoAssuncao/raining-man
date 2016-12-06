from FGAme import *
from boy import Boy
from shot import Shot
from core import randomize, Media, Physics
from pygame.locals import *
import pygame
import os, time

class RainingWorld(World):
	def __init__(self):
		super().__init__()
		self.base_k = 1.05
		self.recover_interval = 150
		self.time_to_exaust = 200
		self.spawn_time = 150
		self.screen_end = -10
		self.shot_list = []
		self.count = 0
		self.points = 0
		self.is_exaust = False
		self.timer = 0 # GAME TIMER
		self.exaustion_timer = 0
		self.recover_timer = 0
		self.vel = (0, 100)

	def add_raining_world(self):
		"""TODO: Docstring for add_raining_world.
		:returns: nothing

		create the objects to the rainging world

		"""

		self.add.margin(200, -500)
		self.gravity = (0, 30)

		self.player = Boy()
		self.player.gravity = (0, 0)
		self.add(self.player)
		shot = Shot() # INITIAL SHOT
		self.shot_list.append(shot)

		pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()

	def start_sound(self):
		"""TODO: Docstring for start_sound.
		Play initial sound to the game

		"""
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()
		Media.change_music("sounds/sound-adventure.mp3")

	def render_game(self):
		pygame.font.init()
		background = Media.change_image('images/background.png')

		text = Media.define_text()
		screen = pygame.display.set_mode((800, 600), 0, 32)
		Media.start_text(screen)


		clock = pygame.time.Clock()
		while True:
			screen.blit(background, (200, 0))
			diff = (self.player.width / 2, self.player.height / 2)
			new_pos = self.player.pos - diff
			screen.blit(self.player.body_pygame.convert_alpha(), 
						new_pos, self.player.rectangle)

			self.update(screen, text)

			for event in pygame.event.get():
				if event.type == QUIT:
					exit()

			pressed_keys = pygame.key.get_pressed()

			if pressed_keys[K_RIGHT]:
				if self.player.pos[0] <= 588:
					self.player.move_p1(2)
			elif pressed_keys[K_LEFT]:
				if self.player.pos[0] >= 215:
					self.player.move_p1(-2)

			if pressed_keys[K_UP]:
				Physics.increase_drag(self)
				self.player.body_pygame = Media.change_image('images/2.png')
			elif not pressed_keys[K_UP] or self.is_exaust:
				self.player.body_pygame = Media.change_image('images/1.png')
				Physics.decrease_drag(self)

			pygame.display.update()
			time_passed = clock.tick(60)

	
	def update(self, screen, text):
		if self.timer >= self.spawn_time:
			self.timer = 0
			self.vel = (0, self.vel[1] + self.count)
			randomize(self.shot_list, self.count, self.vel)

		for shot in self.shot_list:
			new_pos = shot.pos - (shot.width / 2, shot.height / 2)
			screen.blit(shot.body_pygame.convert_alpha(), 
						new_pos)
			shot.update()

			if shot.pos[1] < self.screen_end:
				self.shot_list.remove(shot)
				self.count = self.count + 2
				self.points = self.points + 10 + self.count
				string_points = "%05d" % (self.points)
				Media.update_text(string_points, screen, text)

		def colision():

			# SE o player ta entre a posição + 5 da pedra e entre
			# a posição inferior verifica se colide em x.
			shot_rect = get_surface_rectangle(shot)
			player_rect = get_surface_rectangle(self.player)

			if player_rect.colliderect(shot_rect):
				return True

			return False

		for shot in self.shot_list:
			# END GAME (WORKING!!!!)
			if colision():
				print("GAME OVER")
				Media.change_music('sounds/battle_theme.mp3')
				time.sleep(1)
				exit()

		
		# TIMER INCREASING DEPENDS ON K VALUE
		if not self.shot_list:
			self.timer += 1
		elif (self.shot_list[0].k) == self.base_k:
			self.timer += 1
			if self.exaustion_timer >= self.time_to_exaust:
				self.recover_timer += 1
				if self.recover_timer > self.recover_interval:
					self.exaustion_timer = 0
					self.is_exaust = False
					self.recover_timer = 0
		else: # SLOW DOWN THE TIME
			self.timer += 0.5
			if self.exaustion_timer >= self.time_to_exaust:
				for shot in self.shot_list:
					shot.k = self.base_k
				self.is_exaust = True
			else:
				self.exaustion_timer += 1



def get_surface_rectangle(game_object):
	
	width = game_object.body_pygame.get_width()	
	height = game_object.body_pygame.get_height()

	new_pos = game_object.pos - (game_object.width / 2, game_object.height / 2)

	rect = Rect(new_pos[0], new_pos[1], width - 20, height)

	return rect