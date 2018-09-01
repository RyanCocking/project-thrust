import pygame
import copy

class World:

    def __init__(self):
        self.score=0
        self.kills=0

        self.enemies = []
        self.projectiles = []

        self.screen_width  = 500
        self.screen_height = 400

        self.floor_sprite   = pygame.image.load("images/floor.png")
        self.default_floor_rect     = self.floor_sprite.get_rect()

        floors_in_width=self.screen_width/self.default_floor_rect.width
        floors_in_height=self.screen_height/self.default_floor_rect.height

        self.floor_rects = []
        for x in xrange(floors_in_width+1):
            for y in xrange(floors_in_height+1):
                position=[x*self.default_floor_rect.width,y*self.default_floor_rect.height]
                new_rect=copy.copy(self.default_floor_rect)
                new_rect.x=position[0]
                new_rect.y=position[1]
                self.floor_rects.append(new_rect)

    def draw(self,screen):

        for floor_rect in self.floor_rects:
            screen.blit(self.floor_sprite, floor_rect)
