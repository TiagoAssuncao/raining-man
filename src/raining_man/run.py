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


_ROOT = os.path.abspath(os.path.dirname(__file__))

absolute_image_path = os.path.join(_ROOT, 'sounds/sound-adventure.mp3')
main_sound = pygame.mixer.music.load(absolute_image_path)
main_sound = pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.8);

@listen('long-press', 'up')
def increase_drag():
    if not is_exaust:
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, 'images/2.png')
        for shot in world.shot_list:
            shot.k = 100
    else:
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, 'images/1.png')
        world.player.body_pygame = pygame.image.load('images/1.png')

def decrease_drag():
    for shot in world.shot_list:
        shot.k = world.base_k

@listen('key-down', 'x')
def exit_game():
    exit()



# timers used on update
timer = 0 # GAME TIMER
exaustion_timer = 0
recover_timer = 0

def update(screen, text):
    global timer

    if timer >= world.spawn_time:
        timer = 0
        randomize(world.shot_list)

    for shot in world.shot_list:
        screen.blit(shot.body_pygame.convert_alpha(), 
                    shot.pos, [50, 50, 100, 80])
        shot.update()

        if shot.pos[1] < world.screen_end:
            world.shot_list.remove(shot)
            world.remove(shot)
            global points
            global count
            count = count + 2
            points = points + 10 + count
            string_points = "%05d" % (points)

            point_label = text.get('point').render(
                    string_points,
                    1,
                    text.get('black'))

            screen.fill(text.get('white'))

            # render text
            screen.blit(text.get('tittle'), (10, 50))
            screen.blit(point_label, (10, 80))

    def colision():
        if abs((world.player.body.pos[1])-(shot.pos[1])) < 20:
            if ((world.player.body.pos[0])-(shot.pos[0])) > -25:
                if ((world.player.body.pos[0])-(shot.pos[0])) < 100:
                    return True

        return False

    for shot in world.shot_list:
        # END GAME (WORKING!!!!)
        if colision():
            print("GAME OVER")
            _ROOT = os.path.abspath(os.path.dirname(__file__))
            absolute_image_path = os.path.join(_ROOT, 'sounds/battle_theme.mp3')
            dash_sound =  pygame.mixer.music.load(absolute_image_path)
            dash_sound = pygame.mixer.music.play()
            time.sleep(1)
            exit()

    global exaustion_timer
    global is_exaust
    global recover_timer
    
    # TIMER INCREASING DEPENDS ON K VALUE
    if not world.shot_list:
        timer += 1
    elif (world.shot_list[0].k) == world.base_k:
        timer += 1
        if exaustion_timer >= world.time_to_exaust:
            recover_timer += 1
            if recover_timer > world.recover_interval:
                exaustion_timer = 0
                is_exaust = False
                recover_timer = 0
    else: # SLOW DOWN THE TIME
        timer += 0.5
        if exaustion_timer >= world.time_to_exaust:
            for shot in world.shot_list:
                shot.k = world.base_k
            is_exaust = True
        else:
            exaustion_timer += 1
 

def render_game():
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    absolute_image_path = os.path.join(_ROOT, 'images/background.png')
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
        screen.blit(world.player.body_pygame.convert_alpha(), 
                    world.player.position,world.player.rect)

        update(screen, text)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_RIGHT]:
            if world.player.body.pos[0] <= 575:
                world.player.move_p1(2)
        elif pressed_keys[K_LEFT]:
            if world.player.body.pos[0] >= 200:
                world.player.move_p1(-2)
        else:
            # Do nothing
            pass

        if pressed_keys[K_UP]:
            increase_drag()
        elif not pressed_keys[K_UP] or is_exaust:
            _ROOT = os.path.abspath(os.path.dirname(__file__))
            absolute_image_path = os.path.join(_ROOT, 'images/2.png')
            world.player.body_pygame = pygame.image.load(absolute_image_path)
            decrease_drag()
        else:
            # Do nothing
            pass

        pygame.display.update()
        time_passed = clock.tick(60)


render_game()
