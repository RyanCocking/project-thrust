import numpy as np

# Player class
class Player:

    def __init__(self,position,screen,pygame):
        self.position = position
        self.speed    = 0.12
        self.screen   = screen
        self.sprite   = pygame.image.load("images/player.png")
        self.rect     = self.sprite.get_rect()
        self.rect.x   = self.position[0]
        self.rect.y   = self.position[1]

        # Get screen dimensions
        self.screen_dimensions=[0,0]
        self.screen_dimensions[0],self.screen_dimensions[1]=pygame.display.get_surface().get_size()

        # Screen dimensions adjusted for sprite width
        self.adjusted_screen_dimensions=[0,0]
        self.adjusted_screen_dimensions[0] = self.screen_dimensions[0]-self.rect.width
        self.adjusted_screen_dimensions[1] = self.screen_dimensions[1]-self.rect.height


    def update(self,movement_input):

        # Movement of player
        if np.count_nonzero(movement_input)>0:
            # See if next position is valid

            # Normalise movement vector
            normalised_movement = movement_input / np.linalg.norm(movement_input)
            next_position=self.position+(normalised_movement*self.speed)

            # If next position is valid, move
            if 0<next_position[0]<self.adjusted_screen_dimensions[0]:
                self.position[0]=next_position[0]
                self.rect.x=self.position[0]
            if 0<next_position[1]<self.adjusted_screen_dimensions[1]:
                self.position[1]=next_position[1]
                self.rect.y=self.position[1]

    def draw(self):
        self.screen.blit(self.sprite, self.rect)
