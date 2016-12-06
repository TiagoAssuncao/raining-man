import random
import os
import pygame
from FGAme import *

class Physics(object):

    """Docstring for Physics.
    This class do activicts to world physics.
    """

    def drag(shot):
        x, y = shot.vel
        drag = abs(shot.k * (y ** 2))
        a = (shot.mass * shot.gravity[1] - drag) / shot.mass
        speed_x, speed_y = shot.vel
        speed_y += a * 1/60
        pos_x, pos_y = shot.pos
        pos_y -= speed_y * 1/60

        return (speed_x, speed_y), (pos_x, pos_y)

    @listen('long-press', 'up')
    def increase_drag(world):
        if not world.is_exaust:
            world.player.body_pygame = Media.change_image('images/2.png')
            for shot in world.shot_list:
                shot.k = 100
        else:
            world.player.body_pygame = Media.change_image('images/1.png')

    def decrease_drag(world):
        for shot in world.shot_list:
            shot.k = world.base_k

def randomize(shot_list, count, world_vel):
    for i in range(random.randint(1, 3)):
        from shot import Shot
        shot = Shot()
        count = count + 1
        randomizer = random.randint(-100, 100)
        shot.x = randomizer + random.randint(270, 420)
        shot.y = shot.y + random.randint(-80, -50) # TO NOT GET TOGETHER
        shot_list.append(shot)
        print(world_vel)
        shot.vel = world_vel

class Media():
    @staticmethod
    def change_image(img):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, img)
        return pygame.image.load(absolute_image_path)

    @staticmethod
    def change_music(music):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, music)
        dash_sound =  pygame.mixer.music.load(absolute_image_path)
        dash_sound = pygame.mixer.music.play()

    @staticmethod
    def update_text(string_points, screen, text):
        point_label = text.get('point').render(
                string_points,
                1,
                text.get('black'))

        screen.fill(text.get('white'))

        # render text
        screen.blit(text.get('tittle'), (10, 50))
        screen.blit(point_label, (10, 80))

    @staticmethod
    def define_text():
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        title_font = pygame.font.SysFont("monospace", 25)
        title_label = title_font.render("Raining Man", 1, BLACK)
        point_font = pygame.font.SysFont("monospace", 15)

        text = {
                'white': WHITE,
                'black': BLACK,
                'tittle': title_label,
                'point': point_font,
                }
        return text

    @staticmethod
    def start_text(screen):
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
