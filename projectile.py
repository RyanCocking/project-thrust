import numpy as np
import pygame

class Projectile:

    def __init__(self,position,angle,screen,type):

        self.type         = type
        self.position     = position
        self.angle        = angle
        self.screen       = screen

        self.dead         = False
        self.reflected    = False

        if type == "laser":
            self.sprite       = pygame.transform.rotate(pygame.image.load("images/bullet1.png"),270+angle*(-180.0/np.pi))
            self.speed        = 1
            self.damage       = 5
        elif type == "rocket":
            self.sprite       = pygame.transform.rotate(pygame.image.load("images/rocket1.png"),270+angle*(-180.0/np.pi))
            self.speed        = 2.
            self.damage       = 8

        self.velocity     = np.array([self.speed*np.cos(self.angle),self.speed*np.sin(self.angle)])
        self.rect         = self.sprite.get_rect()


    def update(self,player,world):

        if self.type=="laser":
            self.position += self.velocity
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
        elif self.type=="rocket":

            # Pathfinding
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

            self.position+= normalised_velocity*self.speed
            self.rect.x=self.position[0]
            self.rect.y=self.position[1]

            x_distance=(player.position[0]-self.position[0])
            y_distance=(player.position[1]-self.position[1])

            if x_distance>0:
                self.angle = np.arctan(y_distance/x_distance)
            else:
                self.angle = np.pi+np.arctan(y_distance/x_distance)

            self.sprite       = pygame.transform.rotate(pygame.image.load("images/rocket1.png"),270+self.angle*(-180.0/np.pi))


        # If position is invalid, die
        if not 0<self.position[0]<world.screen_width:
            self.dead=True
        elif not 0<self.position[1]<world.screen_height:
            self.dead=True

    def draw(self,screen,frame_count):
        screen.blit(self.sprite, self.rect)
