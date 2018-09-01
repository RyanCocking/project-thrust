import pygame
import copy
import numpy as np

class World:

    def __init__(self,screen_width,screen_height):
        self.score=0
        self.kills=0

        self.enemies = []
        self.projectiles = []

        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.Font('images/slkscrb.ttf', 30)
        self.wave_text_position=[2*self.screen_width/3.0,0]
        self.score_text_position=[2*self.screen_width/3.0,20]

        self.floor_sprites=[]
        for i in xrange(1,7):
            self.floor_sprites.append(pygame.image.load("images/floor_"+str(i)+".png"))

        self.default_floor_rect     = self.floor_sprites[0].get_rect()

        floors_in_width=self.screen_width/self.default_floor_rect.width
        floors_in_height=self.screen_height/self.default_floor_rect.height

        self.floor_tiles = []
        floor_tile_weightings=[0.7,0.10,0.05,0.05,0.05,0.05]
        for x in xrange(floors_in_width):
            for y in xrange(floors_in_height):
                position=[x*self.default_floor_rect.width,y*self.default_floor_rect.height]
                new_rect=copy.copy(self.default_floor_rect)
                new_rect.x=position[0]
                new_rect.y=position[1]
                floor_tile=[np.random.choice(self.floor_sprites, 1, p=floor_tile_weightings),new_rect]
                self.floor_tiles.append(floor_tile)

        self.wall_sprite=pygame.image.load("images/wall_1.png")
        self.wall_sprite_2=pygame.image.load("images/wall_2.png")
        self.default_wall_rect = self.wall_sprite.get_rect()
        walls_in_width=self.screen_width/self.default_wall_rect.width
        walls_in_height=self.screen_height/self.default_wall_rect.height
        self.wall_tiles=[]
        for y in xrange(walls_in_height):
            position=[0,y*self.default_wall_rect.height]
            new_rect=copy.copy(self.default_wall_rect)
            new_rect.x=position[0]
            new_rect.y=position[1]
            wall_tile=[self.wall_sprite_2,new_rect]
            self.wall_tiles.append(wall_tile)

            position=[self.default_wall_rect.width*(walls_in_width-1),y*self.default_wall_rect.height]
            new_rect=copy.copy(self.default_wall_rect)
            new_rect.x=position[0]
            new_rect.y=position[1]
            wall_tile=[self.wall_sprite_2,new_rect]
            self.wall_tiles.append(wall_tile)

        for x in xrange(walls_in_width):
            position=[x*self.default_wall_rect.width,0]
            new_rect=copy.copy(self.default_wall_rect)
            new_rect.x=position[0]
            new_rect.y=position[1]
            wall_tile=[self.wall_sprite,new_rect]
            self.wall_tiles.append(wall_tile)

            position=[x*self.default_wall_rect.width, self.default_wall_rect.height*(walls_in_height-1)]
            new_rect=copy.copy(self.default_wall_rect)
            new_rect.x=position[0]
            new_rect.y=position[1]
            wall_tile=[self.wall_sprite,new_rect]
            self.wall_tiles.append(wall_tile)


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


    def draw(self,screen,player,waves):

        for floor_tile in self.floor_tiles:
            screen.blit(floor_tile[0][0], floor_tile[1])

        for wall_tile in self.wall_tiles:
            screen.blit(wall_tile[0], wall_tile[1])


        counter=0
        for heart_rect in self.heart_rects:
            if(player.health/10>counter):
                screen.blit(self.heart_sprite, heart_rect)
            else:
                screen.blit(self.empty_heart_sprite, heart_rect)
            counter+=1


        self.wavetextsurface = self.font.render('Wave: '+str(waves.wave_number), False, (0, 0, 0))
        screen.blit(self.wavetextsurface,self.wave_text_position)

        self.scoretextsurface = self.font.render('Score: '+str(self.score), False, (0, 0, 0))
        screen.blit(self.scoretextsurface,self.score_text_position)
