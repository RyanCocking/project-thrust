import numpy as np
import pygame
from projectile import Projectile
# Enemy class

class Enemy:

    def __init__(self,position,screen):
         self.position = position
         self.velocity = np.array([0,0])
         self.speed    = 0.05
         self.screen   = screen
         self.sprite   = pygame.image.load("images/Ballboy_2.png")
         self.rect     = self.sprite.get_rect()
         self.orient   = "down_"
         self.angle    = 0.0
         self.dead     = False
         self.firing_rate = 10
         self.frame    = 0


    def update(self,player,frame_count,world):

        # initilisations
        frame_list = np.array((1,2))

        # Movement
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

        # Animation

        # Stationary
        if (self.velocity[0] == 0) and (self.velocity[1] == 0) and (current_frame%101 == 0):

            current_frame = frame_list[frame_count%2]
            self.sprite = pygame.image.load("images/enemy_rest_" + self.orient + str(current_frame) + ".png")

        # Walking animation
        else:


            current_frame = frame_list[self.frame]

            if (frame_count%51 == 0):

                current_frame = frame_list[self.frame]
                self.frame += 1
                if (self.frame == 2):
                    self.frame = 0

            if self.velocity[1] > 0 or self.velocity[0] > 0:
                self.sprite = pygame.image.load("images/enemy_walk_right_" + str(current_frame) + ".png")
                self.orient = "right_"
            elif self.velocity[1] < 0 or self.velocity[0] < 0:
                self.sprite = pygame.image.load("images/enemy_walk_left_" + str(current_frame) + ".png")
                self.orient = "left_"



    def draw(self):
        self.screen.blit(self.sprite, self.rect)
