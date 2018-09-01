import pygame
import numpy as np
from enemy import Enemy

class Waves:

    def __init__(self,world):

        self.wave_number = 0
        self.boss_wave   = False

    def update(self,world,screen,player,pygame):

        self.wave_number+=1
        self.shooter_number = 2 * self.wave_number
        self.rocket_number = 1 * self.wave_number

        for i in xrange(self.shooter_number):
            # Setup enemy
            enemy_type=0
            distance_from_player=0
            while distance_from_player<20:
                random = np.random.rand(2)
                enemy_start_pos = np.array([world.default_wall_rect.width+(world.screen_width-2.0*world.default_wall_rect.width)*random[0],world.default_wall_rect.height+(world.screen_height-2.0*world.default_wall_rect.height)*random[1]])
                distance_from_player = np.linalg.norm(player.position-enemy_start_pos)
            new_enemy=Enemy(enemy_type,enemy_start_pos,screen)
            world.enemies.append(new_enemy)

        for i in xrange(self.rocket_number):
            # Setup enemy
            enemy_type=1
            distance_from_player=0
            while distance_from_player<20:
                random = np.random.rand(2)
                enemy_start_pos = np.array([world.default_wall_rect.width+(world.screen_width-2.0*world.default_wall_rect.width)*random[0],world.default_wall_rect.height+(world.screen_height-2.0*world.default_wall_rect.height)*random[1]])
                distance_from_player = np.linalg.norm(player.position-enemy_start_pos)
            new_enemy=Enemy(enemy_type,enemy_start_pos,screen)
            world.enemies.append(new_enemy)
