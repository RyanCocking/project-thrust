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

        # Get screen dimensions
        self.screen_dimensions=[0,0]
        self.screen_dimensions[0],self.screen_dimensions[1]=pygame.display.get_surface().get_size()

        # Screen dimensions adjusted for sprite width
        self.adjusted_screen_dimensions=[0,0]
        self.adjusted_screen_dimensions[0] = self.screen_dimensions[0]-self.rect.width
        self.adjusted_screen_dimensions[1] = self.screen_dimensions[1]-self.rect.height


    def update(self,movement_input,pygame,pressed_up,pressed_down,pressed_left,pressed_right,frame_count):
        #print(frame_count)

        # initilisations
        frame_list = np.array((1,2))

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
             if 0<next_position[1]<self.adjusted_screen_dimensions[1]:
                 self.position[1]=next_position[1]
                 self.rect.y=self.position[1]

        # ANIMATION

        # Resting animation
        if (np.array_equal(prev_position,next_position) == True and frame_count%101 == 0):

            current_frame = frame_list[frame_count%2]
            self.sprite = pygame.image.load("images/player_rest_" + self.orient + str(current_frame) + ".png")


        # Walking animation
        else:

            current_frame = frame_list[0]

            if (frame_count%101 == 0):

                current_frame = frame_list[1]

            if pressed_up:
                self.sprite = pygame.image.load("images/player_rest_up_" + str(current_frame) + ".png")
                self.orient = "up_"
            elif pressed_down:
                self.sprite = pygame.image.load("images/player_rest_down_" + str(current_frame) + ".png")
                self.orient = "down_"
            elif pressed_right:
                self.sprite = pygame.image.load("images/player_rest_right_" + str(current_frame) + ".png")
                self.orient = "right_"
            elif pressed_left:
                self.sprite = pygame.image.load("images/player_rest_left_" + str(current_frame) + ".png")
                self.orient = "left_"


    def draw(self):
        self.screen.blit(self.sprite, self.rect)
