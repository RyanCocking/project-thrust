import numpy as np

# Player class
class Player:

    def __init__(self,position,screen,pygame):
        self.position = position
        self.speed    = 0.5
        self.screen   = screen
        self.sprite   = pygame.image.load("images/player.png")
        self.rect     = self.sprite.get_rect()
        self.rect.x   = self.position[0]
        self.rect.y   = self.position[1]
        self.orient   = "down_"

        self.mirror_angle = 0
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


    def update(self,movement_input,pygame,pressed_up,pressed_down,pressed_left,pressed_right,mouse_position,frame_count,world,i):

        # initilisations
        frame_list = np.array((1,2,3,4,3,2))

        # Mouse position gives mirror angle
        x_distance=(mouse_position[0]-self.position[0])
        y_distance=(mouse_position[1]-self.position[1])

        if x_distance>0:
            self.mirror_angle = np.arctan(y_distance/x_distance)
        else:
            self.mirror_angle = np.pi+np.arctan(y_distance/x_distance)

        self.mirror_sprite=pygame.transform.rotate(pygame.image.load("images/mirror.png"),270+self.mirror_angle*(-180.0/np.pi))

        #Store previous position
        prev_position = self.position
        next_position = self.position

        # Movement of player
        if np.count_nonzero(movement_input)>0:
            # See if next position is valid

             #Store previous position
             prev_position = self.position
             next_position = self.position

             # Normalise movement vector
             normalised_movement = movement_input / np.linalg.norm(movement_input)
             next_position=self.position+(normalised_movement*self.speed)

             # If next position is valid, move
             if 0<next_position[0]<self.adjusted_screen_dimensions[0]:
                 self.position[0]=next_position[0]
                 self.rect.x=self.position[0]
                 self.mirror_rect.x=self.position[0]
             if 0<next_position[1]<self.adjusted_screen_dimensions[1]:
                 self.position[1]=next_position[1]
                 self.rect.y=self.position[1]
                 self.mirror_rect.y=self.position[1]


        for projectile in world.projectiles:
            if projectile.rect.contains(self.mirror_rect):
                # Projectile hit mirror, reflect it

                incidence_angle=(90.0-(self.mirror_angle)*(180.0/np.pi)-projectile.angle)
                incidence_angle_rad=incidence_angle*(np.pi/180.0)

                projectile_velocity_magnitude = np.linalg.norm(projectile.velocity)

                projectile.velocity[0] = np.sin(incidence_angle_rad+(projectile.angle*(np.pi/180.0)))*projectile_velocity_magnitude
                projectile.velocity[1] = np.cos(incidence_angle_rad+(projectile.angle*(np.pi/180.0)))*projectile_velocity_magnitude
                projectile.sprite   = pygame.transform.rotate(projectile.sprite,180-incidence_angle_rad+(projectile.angle*(np.pi/180.0)))
                projectile.reflected = True



        # ANIMATION

        # Resting animation
        if (np.array_equal(prev_position,next_position) == True and frame_count%101 == 0):

            current_frame = frame_list[frame_count%2]
            self.sprite = pygame.image.load("images/player_rest_" + self.orient + str(current_frame) + ".png")


        # Walking animation
        else:

            current_frame = frame_list[i]

            if (frame_count%101 == 0):

                current_frame = frame_list[i+1]
                i += 1
                if (i == 5):
                    i = 0

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
