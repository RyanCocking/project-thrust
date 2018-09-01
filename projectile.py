import numpy as np
import pygame

class Projectile:

    def __init__(self,position,angle,screen,type):

        self.type         = type
        self.position     = position
        self.speed        = 1.0
        self.angle        = angle
        self.velocity     = np.array([self.speed*np.cos(self.angle),self.speed*np.sin(self.angle)])
        self.screen       = screen
        self.sprite       = pygame.transform.rotate(pygame.image.load("images/bullet.png"),270+angle*(-180.0/np.pi))
        self.rect         = self.sprite.get_rect()
        self.acceleration = 0
        self.dead         = False
        self.reflected    = False

        #if type == "rocket":
        #    self.acceleration = 0.01
        #    self.speed        = 0.
        if type == "laser":
            self.acceleration = 0
            self.speed        = 1
            self.damage       = 5


    def update(self,world):

        self.position += self.velocity
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        # If position is invalid, die
        if not 0<self.position[0]<world.screen_width:
            self.dead=True
        elif not 0<self.position[1]<world.screen_height:
            self.dead=True

        # if np.count_nonzero(movement_input)>0:
        #     # Movement of player
        #     # See if next position is valid
        #
        #     # Normalise movement vector
        #     normalised_movement = movement_input / np.linalg.norm(movement_input)
        #     next_position=self.position+(normalised_movement*(self.speed+self.acceleration))
        #     self.speed += self.acceleration
        #
        #     # capping projectile speed
        #     if self.speed >= 0.2:
        #         self.acceleration = 0.
        #
        #         # Pathfinding
        #         self.velocity = np.array([0,0])
        #
        #         if self.position[0] > player.position[0]:
        #             self.velocity[0] -= 1
        #         elif self.position[0] < player.position[0]:
        #             self.velocity[0] += 1
        #
        #         if self.position[1] > player.position[1]:
        #             self.velocity[1] -= 1
        #         elif self.position[1] < player.position[1]:
        #             self.velocity[1] += 1
        #
        #         normalised_velocity = self.velocity / np.linalg.norm(self.velocity)
        #
        #         self.position= self.position + normalised_velocity*self.speed
        #         self.rect.x=self.position[0]
        #         self.rect.y=self.position[1]
        #
        #     # If next position is valid, move
        #     if 0<next_position[0]<self.adjusted_screen_dimensions[0]:
        #         self.position[0]=next_position[0]
        #         self.rect.x=self.position[0]
        #     if 0<next_position[1]<self.adjusted_screen_dimensions[1]:
        #         self.position[1]=next_position[1]
        #         self.rect.y=self.position[1]


    def draw(self,screen,frame_count):
        screen.blit(self.sprite, self.rect)
