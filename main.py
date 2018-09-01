import pygame
import numpy as np

from world import World
from waves import Waves
from player import Player
from enemy import Enemy

frame_count = 0
start_state = True
i =0

# Start shit up
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

world=World()
waves=Waves(world)

# Setup screen object, set resolution
screen = pygame.display.set_mode((world.screen_width, world.screen_height))

# Setup player
player_start_pos = np.array([world.screen_width/2.0,world.screen_height/2.0])
player = Player(player_start_pos,screen,pygame)

# Should we stop playing? (No)
done = False

# Keypress bools
pressed_left=False
pressed_right=False
pressed_up=False
pressed_down=False

# While we want to keep playing
while not done:

    frame_count += 1

    # Reset screen
    screen.fill((0,0,0))

    # Movement input vector
    movement_input=np.array([0,0])

    # Check for keyboard events etc
    for event in pygame.event.get():
        # If (x) button of window is clicked
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:          # check for key presses
            if event.key == pygame.K_a:        # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_d:     # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_w:        # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_s:     # down arrow goes down
                pressed_down = True
        elif event.type == pygame.KEYUP:            # check for key releases
            if event.key == pygame.K_a:        # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_d:     # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_w:        # up arrow goes up
                pressed_up = False
            elif event.key == pygame.K_s:     # down arrow goes down
                pressed_down = False

    if pressed_left:
        movement_input[0] -= 1
    if pressed_right:
        movement_input[0] += 1
    if pressed_up:
        movement_input[1] -= 1
    if pressed_down:
        movement_input[1] += 1

    # Do world stuff
    world.draw(screen,player)

    # Do all player stuff
    # Get mouse pos for mirror angle
    mouse_pos = pygame.mouse.get_pos()
    player.update(movement_input,pygame,pressed_up,pressed_down,pressed_left,pressed_right,mouse_pos,frame_count,world,i)
    player.draw()
    if player.dead:
        done=True

    # Do all enemy stuff
    if not world.enemies:
        waves.update(world,screen,player,pygame)
    else:
        for enemy in world.enemies:
            enemy.update(player,frame_count,world)
            enemy.draw()
            if enemy.dead:
                world.enemies.remove(enemy)

    for projectile in world.projectiles:
        projectile.update(world)
        projectile.draw(screen,frame_count)
        if projectile.dead:
            world.projectiles.remove(projectile)

    waves.draw(screen)

    # Redraw the screen
    pygame.display.flip()
    clock.tick(100)
