from FGAme import *
from math import sqrt
import pygame
from pygame.locals import *
from boy import *
from shot import Shot, randomize
import random
import time

#CONSTANTS
BASE_K = 1.05
RECOVER_INTERVAL = 200
TIME_TO_EXAUST = 300
SPAWN_TIME = 130
SCREEN_END = 600

world.add.margin(200, -500)
world.gravity = (0, 30)
PLAYER = Boy()
PLAYER.body.gravity = (0, 0)
gravity_x, gravity_y = PLAYER.body.gravity

shot_list = []
shot = Shot() # INITIAL SHOT
shot_list.append(shot)
count = 0
is_exaust = False

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
main_sound = pygame.mixer.music.load("sounds/sound-adventure.mp3")
main_sound = pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.8);

@listen('long-press', 'up')
def increase_drag():
    if not is_exaust:
        for shot in shot_list:
            shot.k = 100    

@listen('long-press', 'left', dx=-2)
@listen('long-press', 'right', dx=2)
def move_p1(dx):
        PLAYER.body.move(dx, 0)

@listen('key-up', 'up')
def decrease_drag():
    for shot in shot_list:
        shot.k = BASE_K

@listen('key-down', 'x')
def exit_game():
    exit()



# timers used on update
timer = 0 # GAME TIMER
exaustion_timer = 0
recover_timer = 0


@listen ('frame-enter')
def update():
    global timer

    if timer >= SPAWN_TIME:
        timer = 0
        randomize(shot_list)

    for shot in shot_list:
        shot.update()

        if shot.pos[1] > SCREEN_END:
            shot_list.remove(shot)
            world.remove(shot)

    # END GAME
    if PLAYER.body.vel[1] > 0:
        print("GAME OVER")
        dash_sound =  pygame.mixer.music.load("sounds/battle_theme.mp3")
        dash_sound = pygame.mixer.music.play()
        time.sleep(1)
        exit()


    global exaustion_timer
    global is_exaust
    global recover_timer
    
    # TIMER INCREASING DEPENDS ON K VALUE
    if not shot_list:
        timer += 1
    elif (shot_list[0].k) == BASE_K:
        timer += 1
        if exaustion_timer >= TIME_TO_EXAUST:
            recover_timer += 1
            print (recover_timer)
            if recover_timer > RECOVER_INTERVAL:
                exaustion_timer = 0
                is_exaust = False
                recover_timer = 0
    else: # SLOW DOWN THE TIME
        timer += 0.5
        if exaustion_timer >= TIME_TO_EXAUST:
            for shot in shot_list:
                shot.k = BASE_K
            is_exaust = True
        else:
            exaustion_timer += 1
 

def render_game():
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    background = pygame.image.load('images/background.png').convert()

    clock = pygame.time.Clock()
    while True:
        screen.blit(background, (200, 0))
        auxiliar = PLAYER.body_pygame.convert_alpha()
        screen.blit(auxiliar, (400, 80),PLAYER.rect)


        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


        #Habilita as teclas para o controle
        pressed_keys = pygame.key.get_pressed()
        #gravity_influence(PacBum)

        if pressed_keys[K_RIGHT]:
            move_p1(2)
        elif pressed_keys[K_LEFT]:
            move_p1(-2)

        if pressed_keys[K_UP]:
            increase_drag()
        elif not pressed_keys[K_UP]:
            decrease_drag()

        pygame.display.update()
        time_passed = clock.tick(30)


render_game()