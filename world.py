import pygame
import copy
import numpy as np

class World:

    def __init__(self):
        self.score=0
        self.kills=0

        self.enemies = []
        self.projectiles = []

        self.screen_width  = 500
        self.screen_height = 400

        self.floor_sprites=[]
        for i in xrange(1,7):
            self.floor_sprites.append(pygame.image.load("images/floor_"+str(i)+".png"))

        self.default_floor_rect     = self.floor_sprites[0].get_rect()

        floors_in_width=self.screen_width/self.default_floor_rect.width
        floors_in_height=self.screen_height/self.default_floor_rect.height

        self.floor_tiles = []
        floor_tile_weightings=[0.7,0.10,0.05,0.05,0.05,0.05]
        for x in xrange(floors_in_width+1):
            for y in xrange(floors_in_height+1):
                position=[x*self.default_floor_rect.width,y*self.default_floor_rect.height]
                new_rect=copy.copy(self.default_floor_rect)
                new_rect.x=position[0]
                new_rect.y=position[1]
                floor_tile=[np.random.choice(self.floor_sprites, 1, p=floor_tile_weightings),new_rect]
                self.floor_tiles.append(floor_tile)

        self.heart_rects=[]
        self.heart_sprite   = pygame.image.load("images/heart_full.png")
        self.empty_heart_sprite = pygame.image.load("images/heart_empty.png")
        self.heart_rect     = self.heart_sprite.get_rect()

        # 10 hearts positioned along top left of screen
        for i in xrange(10):
           position=[10+i*self.heart_rect.width,5]
           rect=copy.copy(self.heart_rect)
           rect.x=position[0]
           rect.y=position[1]
           self.heart_rects.append(rect)

    def draw(self,screen,player):

        for floor_tile in self.floor_tiles:
            screen.blit(floor_tile[0][0], floor_tile[1])

        counter=0
        for heart_rect in self.heart_rects:
            if(player.health/10>counter):
                screen.blit(self.heart_sprite, heart_rect)
            else:
                screen.blit(self.empty_heart_sprite, heart_rect)
            counter+=1
