import pygame
import numpy as np
from enemy import Enemy

class Waves:

    def __init__(self,world):

        self.wave_number = 0
        self.boss_wave   = False

        self.font = pygame.font.Font('images/slkscrb.ttf', 30)
        self.text_position=[2*world.screen_width/3.0,0]

    def update(self,world,screen,player,pygame):

        self.wave_number+=1
        self.enemy_number = 1* self.wave_number

        for i in xrange(self.enemy_number):
            # Setup enemy
            random = np.random.rand(2)

            distance_from_player=0
            while distance_from_player<40:
                enemy_start_pos = np.array([world.screen_width*random[0],world.screen_height*random[1]])
                distance_from_player = np.linalg.norm(player.position-enemy_start_pos)
            new_enemy=Enemy(enemy_start_pos,screen)
            world.enemies.append(new_enemy)

    def draw(self,screen):
        self.textsurface = self.font.render('Wave: '+str(self.wave_number), False, (0, 0, 0))
        screen.blit(self.textsurface,self.text_position)
