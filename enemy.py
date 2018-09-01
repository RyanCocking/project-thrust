import numpy as np
import pygame
from projectile import Projectile
# Enemy class

class Enemy:

    def __init__(self,position,screen):
         self.position = position
         self.velocity = np.array([0,0])
         self.speed    = 0.1
         self.screen   = screen
         self.sprite   = pygame.image.load("images/Ballboy_2.png")
         self.rect     = self.sprite.get_rect()
         self.orient   = "down_"
         self.angle    = 0.0
         self.dead     = False
         self.health   = 100
         self.firing_rate = 90
         self.draw_damage_text=False
         self.draw_timer = 0
         self.frame    = 0

         self.font = pygame.font.Font('images/slkscre.ttf', 25)

    def update(self,player,frame_count,world):

        # initilisations
        frame_list = np.array((1,2))

        self.firing_rate = 90+int(np.random.rand()*1)

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
                random_damage=np.random.rand(1)*4
                total_damage=projectile.damage+random_damage
                self.health-=total_damage
                self.damage_taken=int(total_damage)
                self.draw_damage_text=True
                projectile.dead=True
                world.projectiles.remove(projectile)

        if self.health<=0:
            self.dead=True
            world.score+=5

        if self.draw_damage_text:
            self.draw_timer+=100
            if self.draw_timer>3000:
                self.draw_timer=0
                self.draw_damage_text=False

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

        if(self.draw_damage_text):
            self.textsurface = self.font.render(str(self.damage_taken), False, (0, 0, 0))
            self.textsurface.set_alpha(255-self.draw_timer/50)
            self.screen.blit(self.textsurface,self.position-[0,0.01*self.draw_timer])
