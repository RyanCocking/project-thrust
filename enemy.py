import pygame
import numpy as np
from projectile import Projectile

# Enemy class

class Enemy:

    def __init__(self,position,screen):
         self.position = position
         self.velocity = np.array([0,0])
         self.speed    = 0.05
         self.angle    = 0.0
         self.dead     = False
         self.firing_rate = 90
         self.screen   = screen
         self.sprite   = pygame.image.load("images/Ballboy_2.png")
         self.rect     = self.sprite.get_rect()
         self.orient   = "down_"


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

            current_frame = frame_list[0]

            if (frame_count%101 == 0):

                current_frame = frame_list[1]

            if self.velocity[1] > 0:
                self.sprite = pygame.image.load("images/player_rest_up_" + str(current_frame) + ".png")
                self.orient = "up_"
            elif self.velocity[1] < 0:
                self.sprite = pygame.image.load("images/player_rest_down_" + str(current_frame) + ".png")
                self.orient = "down_"
            elif self.velocity[0] > 0:
                self.sprite = pygame.image.load("images/player_rest_right_" + str(current_frame) + ".png")
                self.orient = "right_"
            elif self.velocity[0] < 0:
                self.sprite = pygame.image.load("images/player_rest_left_" + str(current_frame) + ".png")
                self.orient = "left_"

        x_distance=(player.position[0]-self.position[0])
        y_distance=(player.position[1]-self.position[1])

        if x_distance>0:
            self.angle = np.arctan(y_distance/x_distance)
        else:
            self.angle = np.pi+np.arctan(y_distance/x_distance)

        # Shooting
        if frame_count%self.firing_rate==0:
            new_bullet = Projectile(self.position,self.angle,self.screen,"laser")
            world.projectiles.append(new_bullet)

        # Getting shot
        for projectile in world.projectiles:
            if self.rect.colliderect(projectile.rect) and projectile.reflected:
                self.dead=True


    def draw(self):
        self.screen.blit(self.sprite, self.rect)
