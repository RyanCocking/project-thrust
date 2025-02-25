import pygame

class Loot:

    def __init__(self,position,type):

        self.position=position
        self.type=type

        if self.type==0:
            # Health
            self.sprite=pygame.image.load("images/health.png")

        self.rect = self.sprite.get_rect()
        self.rect.x=self.position[0]
        self.rect.y=self.position[1]

    def pickup(self,player,world):

        if self.type==0:
            # health
            player.health+=20
            if player.health>player.max_health:
                player.health=player.max_health


        world.pickups.remove(self)

    def draw(self,screen):
        screen.blit(self.sprite, self.rect)
