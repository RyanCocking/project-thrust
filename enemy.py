import numpy as np

# Enemy class

class Enemy:

    def __init__(self,position,screen,pygame):
         self.position = position
         self.velocity = np.array([0,0])
         self.speed    = 0.05
         self.screen   = screen
         self.sprite   = pygame.image.load("images/Ballboy_2.png")
         self.rect     = self.sprite.get_rect()


    def update(self,player):

        self.velocity = np.array([0,0])

        if self.position[0] > player.position[0]:
            self.velocity[0] -= 1
        elif self.position[0] < player.position[0]:
            self.velocity[0] += 1

        if self.position[1] > player.position[1]:
            self.velocity[1] -= 1
        elif self.position[1] < player.position[1]:
            self.velocity[1] += 1

        normalised_velocity = self.velocity / np.linalg.norm(self.velocity)

        self.position= self.position + normalised_velocity*self.speed
        self.rect.x=self.position[0]
        self.rect.y=self.position[1]

    def draw(self):
        self.screen.blit(self.sprite, self.rect)
