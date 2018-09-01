import numpy as np
from enemy import Enemy

class Waves:

    def __init__(self):

        self.wave_number = 0
        self.boss_wave   = False

    def update(self,world,screen,pygame):

        self.wave_number+=1
        self.enemy_number = 1* self.wave_number

        for i in xrange(self.enemy_number):
            # Setup enemy
            random = np.random.rand(2)
            enemy_start_pos = np.array([world.screen_width*random[0],world.screen_height*random[1]])
            new_enemy=Enemy(enemy_start_pos,screen)
            world.enemies.append(new_enemy)
