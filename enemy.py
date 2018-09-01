import numpy as np
import pygame
import copy
from projectile import Projectile
# Enemy class

class Enemy:

    def __init__(self,type,position,screen):

         self.type=type

         if self.type==0: #Shooters
             self.sprite   = pygame.image.load("images/enemy_init_1.png")
             self.speed_original = 0.5
             self.health   = 25
             self.firing_rate_original = 100
         elif self.type==1: # Rocket lads
             self.sprite   = pygame.image.load("images/Trongle_L1.png")
             self.speed_original = 0.35
             self.health   = 40
             self.firing_rate_original = 150

         self.position = position
         self.velocity = np.array([0,0])

         self.speed    = self.speed_original
         self.screen   = screen

         self.rect     = self.sprite.get_rect()
         self.orient   = "left_"
         self.angle    = 0.0
         self.dead     = False
<<<<<<< HEAD


=======
         self.health   = 25
         self.firing_rate_original = 20
>>>>>>> be48692310772df183957b9f0c9432eb1435925b
         self.firing_rate = self.firing_rate_original
         self.draw_damage_text=False
         self.draw_timer = 0
         self.frame    = 0
         self.teleport = True
         self.tele_count = 1
         self.charging  = 1

         self.chasing=True
         self.fleeing=False
         self.fleeing_counter=0
         self.retarget_counter=0

         self.font = pygame.font.Font('images/slkscre.ttf', 25)

         # Get screen dimensions
         self.screen_dimensions=[0,0]
         self.screen_dimensions[0],self.screen_dimensions[1]=pygame.display.get_surface().get_size()

         # Screen dimensions adjusted for sprite width
         self.adjusted_screen_dimensions=[0,0]
         self.adjusted_screen_dimensions[0] = self.screen_dimensions[0]-self.rect.width
         self.adjusted_screen_dimensions[1] = self.screen_dimensions[1]-self.rect.height

    def update(self,player,frame_count,world):
        # initilisations
        frame_list = np.array((1,2))

        self.firing_rate = self.firing_rate_original+int(np.random.rand()*1)

        # Movement
        self.velocity = np.array([0,0])

        if(self.retarget_counter%100==0):
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
        self.retarget_counter+=1

        if self.chasing:
            if self.position[0] > self.target_position[0]:
                self.velocity[0] -= 1
            elif self.position[0] < self.target_position[0]:
                self.velocity[0] += 1

            if self.position[1] > self.target_position[1]:
                self.velocity[1] -= 1
            elif self.position[1] < self.target_position[1]:
                self.velocity[1] += 1

        elif self.fleeing:
            if self.position[0] > self.target_position[0]:
                self.velocity[0] += 1
            elif self.position[0] < self.target_position[0]:
                self.velocity[0] -= 1

            if self.position[1] > self.target_position[1]:
                self.velocity[1] += 1
            elif self.position[1] < self.target_position[1]:
                self.velocity[1] -= 1

            self.fleeing_counter+=1
            if self.fleeing_counter>500:
                self.chasing=True
                self.fleeing=False
                self.fleeing_counter=0

        normalised_velocity = self.velocity / np.linalg.norm(self.velocity)
        next_position= self.position + normalised_velocity*self.speed

        # If next position is valid, move
        if world.default_wall_rect.width<next_position[0]<self.adjusted_screen_dimensions[0]-world.default_wall_rect.width:
            self.position[0]=next_position[0]
            self.rect.x=self.position[0]

        if world.default_wall_rect.height<next_position[1]<self.adjusted_screen_dimensions[1]-world.default_wall_rect.height:
            self.position[1]=next_position[1]
            self.rect.y=self.position[1]


        if self.teleport == False:
            # Animation
            # Stationary
            if (all(self.velocity== 0) and (current_frame%101 == 0)):
                current_frame = frame_list[frame_count%2]
                if self.type==0:
                    self.sprite = pygame.image.load("images/enemy_rest_" + self.orient + str(current_frame) + ".png")

            # Walking animation
            else:
                current_frame = frame_list[self.frame]
                self.frame += 1
                if (self.frame == 2):
                    self.frame = 0

                if self.position[0]-self.prev_position[0] > 10:
                    if self.type==0:
                        self.sprite = pygame.image.load("images/enemy_walk_right_" + str(current_frame) + ".png")
                    self.orient = "right_"
                elif self.position[0]-self.prev_position[0] < -10:
                    if self.type==0:
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



            current_frame = frame_list[self.frame]
            self.frame += 1
            if (self.frame == 2):
                self.frame = 0

            if self.charging < 4:
                self.sprite = pygame.image.load("images/enemy_charge_"+self.orient + str(current_frame) + ".png")
                self.charging+=1
                print (current_frame)

            if self.charging >= 4:
                bullet_position=copy.copy(self.position)
                bullet_angle=copy.copy(self.angle)
                if self.type==0:
                    bullet_type="laser"
                elif self.type==1:
                    bullet_type="rocket"
                new_bullet = Projectile(bullet_position,bullet_angle,self.screen,bullet_type)
                world.projectiles.append(new_bullet)
                self.charging = 0


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
                self.chasing=False
                self.fleeing=True

        if self.health<=0:
            self.dead=True
            world.score+=5

        if self.draw_damage_text:
            self.draw_timer+=100
            if self.draw_timer>3000:
                self.draw_timer=0
                self.draw_damage_text=False

        self.prev_position=self.position

    def draw(self,frame_count):
        self.screen.blit(self.sprite, self.rect)

        if(self.draw_damage_text):
            self.textsurface = self.font.render(str(self.damage_taken), False, (0, 0, 0))
            self.textsurface.set_alpha(255-self.draw_timer/50)
            self.screen.blit(self.textsurface,self.position-[0,0.01*self.draw_timer])


        if(self.teleport):
            self.firing_rate = 1e9
            self.speed       = 0.
            if (frame_count%7 == 0):
                if self.type==0:
                    self.sprite = pygame.image.load("images/enemy_init_" + str(self.tele_count) + ".png")
                self.tele_count += 1

            if (self.tele_count == 9):
                self.firing_rate = self.firing_rate_original
                self.speed       = self.speed_original
                self.teleport    = False
