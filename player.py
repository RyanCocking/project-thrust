# Player class

class Player:

    def __init__(self,position,pygame):
        self.position = position
        self.sprite   = pygame.image.load("images/player.png")
        self.rect     = self.sprite.get_rect()

    def update(self,movement_input):
       next_position=self.position+movement_input
       self.position=next_position

       self.rect.x=self.position[0]
       self.rect.y=self.position[1]

    def draw(self,screen):
        screen.blit(self.sprite, self.rect)
