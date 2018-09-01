import numpy as np
from projectile import Projectile

# Enemy class

class Enemy:

    def __init__(self,position,screen,pygame):
         self.position = position
         self.velocity = np.array([0,0])
         self.speed    = 0.5
         self.angle    = 0.0
         self.firing_rate = 60

         self.screen   = screen
         self.sprite   = pygame.image.load("images/Ballboy_2.png")
         self.rect     = self.sprite.get_rect()


    def update(self,frame_count,player,world):

        # Movement stuff ---------------------------------------------------
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

        x_distance=(player.position[0]-self.position[0])
        y_distance=(player.position[1]-self.position[1])

        if x_distance>0:
            self.angle = np.arctan(y_distance/x_distance)
        else:
            self.angle = np.pi+np.arctan(y_distance/x_distance)

        #--------------------------------------------------------------------------

        # Shooting
        if frame_count%self.firing_rate==0:
            new_bullet = Projectile(self.position,self.angle,self.screen,"laser")
            world.projectiles.append(new_bullet)


    def draw(self):
        self.screen.blit(self.sprite, self.rect)
