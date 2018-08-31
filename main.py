import pygame

# Start shit up
pygame.init()

# Setup screen object, set resolution
screen = pygame.display.set_mode((1366, 768))

# Should we stop playing? (No)
done = False

# While we want to keep playing
while not done:

    # Check for keyboard events etc
    for event in pygame.event.get():
        # If (x) button of window is clicked
        if event.type == pygame.QUIT:
            done = True

    # Redraw the screen
    pygame.display.flip()
