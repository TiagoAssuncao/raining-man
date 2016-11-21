"""
NOT USED YET.
"""

from FGAme import *
from boy import Boy
from shot import Shot, randomize
from pygame.locals import *
import pygame
import os, time

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
        self.root = os.path.abspath(os.path.dirname(__file__))
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
        self.player.body.gravity = (0, 0)
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
        music_path = self.root + "/sounds/sound-adventure.mp3"
        main_sound = pygame.mixer.music.load(music_path)
        main_sound = pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.8)

    def render_game(self):
        pygame.font.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        absolute_image_path = os.path.join(self.root, 'images/background.png')
        background = pygame.image.load(absolute_image_path).convert()

        # initialize font;
        title_font = pygame.font.SysFont("monospace", 25)
        point_font = pygame.font.SysFont("monospace", 15)
        
        #define colors
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        #define text
        title_label = title_font.render("Raining Man", 1, BLACK)
        point_label = point_font.render("00000", 1, BLACK)

        screen.fill(WHITE)

        # render text
        screen.blit(title_label, (10, 50))
        screen.blit(point_label, (10, 80))

        text = {
                'white': WHITE,
                'black': BLACK,
                'tittle': title_label,
                'point': point_font,
                }

        clock = pygame.time.Clock()
        while True:
            screen.blit(background, (200, 0))
            screen.blit(self.player.body_pygame.convert_alpha(), 
                        self.player.position, self.player.rect)

            self.update(screen, text)

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_RIGHT]:
                if self.player.body.pos[0] <= 575:
                    self.player.move_p1(2)
            elif pressed_keys[K_LEFT]:
                if self.player.body.pos[0] >= 200:
                    self.player.move_p1(-2)

            if pressed_keys[K_UP]:
                self.increase_drag()
                absolute_image_path = os.path.join(self.root, 'images/2.png')
                self.player.body_pygame = pygame.image.load(absolute_image_path)
            elif not pressed_keys[K_UP] or self.is_exaust:
                absolute_image_path = os.path.join(self.root, 'images/1.png')
                self.player.body_pygame = pygame.image.load(absolute_image_path)
                self.decrease_drag()

            pygame.display.update()
            time_passed = clock.tick(60)

    
    def update(self, screen, text):
        if self.timer >= self.spawn_time:
            self.timer = 0
            self.vel = (0, self.vel[1] + self.count)
            randomize(self.shot_list, self.count, self.vel)

        for shot in self.shot_list:
            screen.blit(shot.body_pygame.convert_alpha(), 
                        shot.pos, [50, 50, 100, 80])
            shot.update()

            if shot.pos[1] < self.screen_end:
                self.shot_list.remove(shot)
                self.count = self.count + 2
                self.points = self.points + 10 + self.count
                string_points = "%05d" % (self.points)

                point_label = text.get('point').render(
                        string_points,
                        1,
                        text.get('black'))

                screen.fill(text.get('white'))

                # render text
                screen.blit(text.get('tittle'), (10, 50))
                screen.blit(point_label, (10, 80))

        def colision():
            if abs((self.player.body.pos[1])-(shot.pos[1])) < 20:
                if ((self.player.body.pos[0])-(shot.pos[0])) > -25:
                    if ((self.player.body.pos[0])-(shot.pos[0])) < 100:
                        return True

            return False

        for shot in self.shot_list:
            # END GAME (WORKING!!!!)
            if colision():
                print("GAME OVER")
                absolute_image_path = os.path.join(self.root, 'sounds/battle_theme.mp3')
                dash_sound =  pygame.mixer.music.load(absolute_image_path)
                dash_sound = pygame.mixer.music.play()
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

    @listen('long-press', 'up')
    def increase_drag(self):
        if not self.is_exaust:
            absolute_image_path = os.path.join(self.root, 'images/2.png')
            for shot in self.shot_list:
                shot.k = 100
        else:
            absolute_image_path = os.path.join(self.root, 'images/1.png')
            self.player.body_pygame = pygame.image.load(absolute_image_path)

    def decrease_drag(self):
        for shot in self.shot_list:
            shot.k = self.base_k
