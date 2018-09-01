import pygame
import numpy as np

from player import Player
from enemy import Enemy

# Start shit up
pygame.init()

# Setup screen object, set resolution
screen_width  = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# Setup player
player_start_pos = np.array([screen_width/2.0,screen_height/2.0])
player = Player(player_start_pos,screen,pygame)

# Setup enemy
enemy_start_pos = np.array([100,100])
enemy = Enemy(enemy_start_pos,screen,pygame)

# Should we stop playing? (No)
done = False

# Keypress bools
pressed_left=False
pressed_right=False
pressed_up=False
pressed_down=False

# While we want to keep playing
while not done:

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
            if event.key == pygame.K_LEFT:        # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_RIGHT:     # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_UP:        # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_DOWN:     # down arrow goes down
                pressed_down = True
        elif event.type == pygame.KEYUP:            # check for key releases
            if event.key == pygame.K_LEFT:        # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_RIGHT:     # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_UP:        # up arrow goes up
                pressed_up = False
            elif event.key == pygame.K_DOWN:     # down arrow goes down
                pressed_down = False

    if pressed_left:
        movement_input[0] -= 1
    if pressed_right:
        movement_input[0] += 1
    if pressed_up:
        movement_input[1] -= 1
    if pressed_down:
        movement_input[1] += 1

    # Do all updating
    player.update(movement_input)
    enemy.update(player)

    # Do all drawing
    player.draw()
    enemy.draw()

    # Redraw the screen
    pygame.display.flip()
