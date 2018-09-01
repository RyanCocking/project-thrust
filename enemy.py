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
         self.rect.x   = self.position[0]
         self.rect.y   = self.position[1]


    def update(self,player):

        self.velocity = np.array([0,0])

        # Target position in ring around player
        R1=1.0
        R2=0.2
        r1= R1/R1
        r2= R2/R1

        t = 2.0*np.pi*np.random.rand()
        u = np.random.rand() + np.random.rand()
        if u>1.0:
            r=2.0-u
        else:
            r=u
        if r<r2:
            r = r2+(r*((R1-R2)/R2))*R1
        r = r*R1*1000

        self.target_position = np.array([r*np.cos(t)+player.position[0],r*np.sin(t)+player.position[1]])

        if self.position[0] > self.target_position[0]:
            self.velocity[0] -= 1
        elif self.position[0] < self.target_position[0]:
            self.velocity[0] += 1

        if self.position[1] > self.target_position[1]:
            self.velocity[1] -= 1
        elif self.position[1] < self.target_position[1]:
            self.velocity[1] += 1



        normalised_velocity = self.velocity / np.linalg.norm(self.velocity)

        self.position= self.position + normalised_velocity*self.speed
        self.rect.x=self.position[0]
        self.rect.y=self.position[1]

    def draw(self):
        self.screen.blit(self.sprite, self.rect)
