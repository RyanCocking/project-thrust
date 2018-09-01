import numpy as np

from world import World
from waves import Waves
from player import Player
from enemy import Enemy

def main(pygame,screen,screen_width,screen_height,font,text_position):

    frame_count = 0
    start_state = True

    clock = pygame.time.Clock()

    world=World(screen_width,screen_height)
    waves=Waves(world)

    # Setup screen object, set resolution
    screen = pygame.display.set_mode((world.screen_width, world.screen_height))

    # Setup player
    player_start_pos = np.array([world.screen_width/2.0,world.screen_height/2.0])
    player = Player(player_start_pos,screen)

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
        world.draw(screen,player,waves)

        # Do all player stuff
        # Get mouse pos for mirror angle
        mouse_pos = pygame.mouse.get_pos()
        player.update(movement_input,pygame,pressed_up,pressed_down,pressed_left,pressed_right,mouse_pos,frame_count,world)
        player.draw()
        if player.dead:
            done=True

        # Do all enemy stuff
        if not world.enemies:
            waves.update(world,screen,player,pygame)
        else:
            for enemy in world.enemies:
                enemy.update(player,frame_count,world)
                enemy.draw(frame_count)
                if enemy.dead:
                    world.enemies.remove(enemy)

        for loot in world.pickups:
            loot.draw(screen)

        for projectile in world.projectiles:
            projectile.update(player,world)
            projectile.draw(screen,frame_count)
            if projectile.dead:
                world.projectiles.remove(projectile)

        # Redraw the screen
        pygame.display.flip()
        clock.tick(100)

    textsurface = font.render('Game Over!', False, (255, 255, 255))
    text_position=[60,world.screen_height/4.0]
    textsurface_wave = font.render('Wave: '+str(waves.wave_number), False, (255, 255, 255))
    text_position_wave=[60,world.screen_height/2.0]
    textsurface_score = font.render('Score: '+str(world.score), False, (255, 255, 255))
    text_position_score=[60,3*world.screen_height/4.0]
    while done:
        # Reset screen
        screen.fill((0,0,0))
        screen.blit(textsurface,text_position)
        screen.blit(textsurface_wave,text_position_wave)
        screen.blit(textsurface_score,text_position_score)
        pygame.display.flip()

        for event in pygame.event.get():
            # If (x) button of window is clicked
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                done = False
