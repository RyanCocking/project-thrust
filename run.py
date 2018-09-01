import main
import pygame

# Start shit up
pygame.init()
pygame.font.init()

screen_width=700
screen_height=500

screen = pygame.display.set_mode((screen_width, screen_height))

done=False
play=False

font = pygame.font.Font('images/slkscrb.ttf',35)
text_position=[40,screen_height/2.0]
textsurface = font.render('Press any key to play...', False, (255, 255, 255))

while not done:
    # Check for keyboard events etc
    for event in pygame.event.get():
        # If (x) button of window is clicked
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:          # check for key presses
            play=True
            done=True
    screen.blit(textsurface,text_position)
    pygame.display.flip()

if play:
    main.main(pygame,screen,screen_width,screen_height,font,text_position)
