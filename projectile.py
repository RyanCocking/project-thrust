import numpy as np

class Projectile:

    def __init__(self,position,screen,type):

        self.type         = type
        self.position     = position
        self.speed        = 0.12
        self.screen       = screen
        self.sprite       = pygame.image.load("images/" + type + "1.png")
        self.rect         = self.sprite.get_rect()
        self.acceleration = 0

        if type == "rocket":

            self.acceleration = 0.01
            self.speed        = 0.


    def update(self,movement_input):
        # Store previous position
        prev_position = self.position

        if np.count_nonzero(movement_input)>0:
            # Movement of player
            # See if next position is valid

            # Normalise movement vector
            normalised_movement = movement_input / np.linalg.norm(movement_input)
            next_position=self.position+(normalised_movement*(self.speed+self.acceleration))
            self.speed += self.acceleration

            # capping projectile speed
            if self.speed == 0.2:
                self.acceleration = 0.

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

                self.position= self.position + normalised_velocity*self.speed
                self.rect.x=self.position[0]
                self.rect.y=self.position[1]

            # If next position is valid, move
            if 0<next_position[0]<self.adjusted_screen_dimensions[0]:
                self.position[0]=next_position[0]
                self.rect.x=self.position[0]
            if 0<next_position[1]<self.adjusted_screen_dimensions[1]:
                self.position[1]=next_position[1]
                self.rect.y=self.position[1]


    def draw(self,screen,frame_count):

        # initilisations
        im_index    = np.array(1,2,1)


        screen.blit(self.sprite, self.rect)

        # animation
        for i in rest_im_index:
            self.sprite = pygame.image.load("images/" + self.type + str(i)) + ".png"
