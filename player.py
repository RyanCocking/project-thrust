import numpy as np
import pygame

# Player class
class Player:

    def __init__(self,position,screen):
        self.position = position
        self.speed    = 0.5
        self.screen   = screen
        self.sprite   = pygame.image.load("images/player.png")
        self.rect     = self.sprite.get_rect()
        self.rect.x   = self.position[0]
        self.rect.y   = self.position[1]
        self.orient   = "down_"
        self.frame    = 0

        self.health   = 100
        self.dead     = False

        self.mirror_angle = 0
        self.mirror_distance = 25
        self.mirror_offset = np.array([np.cos(self.mirror_angle),np.sin(self.mirror_angle)])*self.mirror_distance
        self.mirror_sprite = pygame.image.load("images/mirror.png")
        self.mirror_rect = self.mirror_sprite.get_rect()
        self.mirror_rect.x = self.position[0]
        self.mirror_rect.y = self.position[1]

        # Get screen dimensions
        self.screen_dimensions=[0,0]
        self.screen_dimensions[0],self.screen_dimensions[1]=pygame.display.get_surface().get_size()

        # Screen dimensions adjusted for sprite width
        self.adjusted_screen_dimensions=[0,0]
        self.adjusted_screen_dimensions[0] = self.screen_dimensions[0]-self.rect.width
        self.adjusted_screen_dimensions[1] = self.screen_dimensions[1]-self.rect.height

        self.font = pygame.font.Font('images/slkscre.ttf', 25)
        self.draw_damage_text=False
        self.draw_timer = 0
        self.damage_taken = 0


    def update(self,movement_input,pygame,pressed_up,pressed_down,pressed_left,pressed_right,mouse_position,frame_count,world):

        # initilisations
        frame_list = np.array((1,2,3,4))

        # Mouse position gives mirror angle
        x_distance=(mouse_position[0]-self.position[0])
        y_distance=(mouse_position[1]-self.position[1])

        if x_distance>0:
            self.mirror_angle = np.arctan(y_distance/x_distance)
        else:
            self.mirror_angle = np.pi+np.arctan(y_distance/x_distance)

        self.mirror_offset = np.array([np.cos(self.mirror_angle),np.sin(self.mirror_angle)])*self.mirror_distance
        self.mirror_sprite=pygame.transform.rotate(pygame.image.load("images/mirror.png"),90+self.mirror_angle*(-180.0/np.pi))

        #Store previous position
        prev_position = self.position
        next_position = self.position

        self.recoil=[0,0]
        for projectile in world.projectiles:
            if projectile.rect.colliderect(self.mirror_rect) and projectile.reflected!=True:
                # Projectile hit mirror, reflect it
                self.recoil[0]=projectile.velocity[0]*2
                self.recoil[1]=projectile.velocity[1]*2

                incidence_angle=(90.0-(self.mirror_angle)*(180.0/np.pi)-projectile.angle)
                incidence_angle_rad=incidence_angle*(np.pi/180.0)

                projectile_velocity_magnitude = np.linalg.norm(projectile.velocity)

                projectile.velocity[0] = np.sin(incidence_angle_rad+(projectile.angle*(np.pi/180.0)))*projectile_velocity_magnitude
                projectile.velocity[1] = np.cos(incidence_angle_rad+(projectile.angle*(np.pi/180.0)))*projectile_velocity_magnitude
                projectile.sprite   = pygame.transform.rotate(projectile.sprite,180-incidence_angle_rad+(projectile.angle*(np.pi/180.0)))
                projectile.reflected = True


            if projectile.rect.colliderect(self.rect):
                random_damage=np.random.rand(1)*4
                total_damage=projectile.damage+random_damage
                self.health-=total_damage
                self.damage_taken=int(total_damage)
                self.draw_damage_text=True
                projectile.dead=True
                self.recoil[0]=projectile.velocity[0]*3
                self.recoil[1]=projectile.velocity[1]*3
                world.projectiles.remove(projectile)

        # Movement of player
        next_position=self.position+self.recoil
        if np.count_nonzero(movement_input)>0:
            # See if next position is valid

             #Store previous position
             prev_position = self.position

             # Normalise movement vector
             normalised_movement = movement_input / np.linalg.norm(movement_input)
             next_position+=(normalised_movement*self.speed)

        # If next position is valid, move
        if world.default_wall_rect.width<next_position[0]<self.adjusted_screen_dimensions[0]-world.default_wall_rect.width:
            self.position[0]=next_position[0]
            self.rect.x=self.position[0]

        if world.default_wall_rect.height<next_position[1]<self.adjusted_screen_dimensions[1]-world.default_wall_rect.height:
            self.position[1]=next_position[1]
            self.rect.y=self.position[1]

        self.mirror_rect.x=self.position[0]+self.mirror_offset[0]
        self.mirror_rect.y=self.position[1]+self.mirror_offset[1]

        if self.health<1:
            self.dead=True

        if self.draw_damage_text:
            self.draw_timer+=100
            if self.draw_timer>3000:
                self.draw_timer=0
                self.draw_damage_text=False

        # ANIMATION

        # Resting animation
        if (np.array_equal(prev_position,next_position) == True and frame_count%101 == 0):

            current_frame = frame_list[frame_count%2]
            self.sprite = pygame.image.load("images/player_rest_" + self.orient + str(current_frame) + ".png")

        # Walking animation
        else:
            current_frame = frame_list[self.frame]

            if (frame_count%51 == 0):

                current_frame = frame_list[self.frame]
                self.frame += 1
                if (self.frame == 4):
                    self.frame = 0

            if pressed_up:
                self.sprite = pygame.image.load("images/player_walk_up_" + str(current_frame) + ".png")
                self.orient = "up_"
            elif pressed_down:
                self.sprite = pygame.image.load("images/player_walk_down_" + str(current_frame) + ".png")
                self.orient = "down_"
            elif pressed_right:
                self.sprite = pygame.image.load("images/player_walk_right_" + str(current_frame) + ".png")
                self.orient = "right_"
            elif pressed_left:
                self.sprite = pygame.image.load("images/player_walk_left_" + str(current_frame) + ".png")
                self.orient = "left_"


    def draw(self):
        self.screen.blit(self.sprite, self.rect)
        self.screen.blit(self.mirror_sprite, self.mirror_rect)

        if(self.draw_damage_text):
            self.textsurface = self.font.render(str(self.damage_taken), False, (255, 38, 0))
            self.textsurface.set_alpha(255-self.draw_timer/50)
            self.screen.blit(self.textsurface,self.position-[0,0.01*self.draw_timer])
