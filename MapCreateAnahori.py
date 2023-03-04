"""

迷路自動生成アルゴリズム
穴掘り法

"""
import numpy as np
import random

class Anahori:
    def __init__(self, map_size=(100, 100), create_size=1000, layer_num=10):
        self.floor = 0
        self.wall = 1
        self.lower_stairs = 2
        self.player_id = 10
        self.map_size = map_size
        self.create_size = create_size
        self.layer_num = layer_num
        self.map_init()
        self.player_current = self.start_point
    
    def clear(self):
        self.map_list = np.ones(shape=self.map_size, dtype='int')
    
    def set_start_point(self):
        self.start_point = (
            np.random.randint(0, self.map_size[0]),
            np.random.randint(0, self.map_size[1])
        )
        
    def map_init(self):
        self.clear()
        self.set_start_point()
    
    def set_player(self):
        self.map_list[self.start_point] += self.player_id
        self.player_current = self.start_point
    
    def set_lower_stairs(self):
        while True:
            self.lower_stairs_point = (
                np.random.randint(0, self.map_size[0]),
                np.random.randint(0, self.map_size[1])
            )
            if self.map_list[self.lower_stairs_point] == self.floor:
                self.map_list[self.lower_stairs_point] = self.lower_stairs
                break

    def create(self):
        self.map_init()
        for _ in range(self.layer_num):
            origin = np.asarray(self.start_point)
            for _ in range(self.create_size):
                direction = random.choice([
                    np.array([-1, 0]),
                    np.array([0, 1]),
                    np.array([1, 0]),
                    np.array([0, -1])
                ])
                tmp = origin + direction
                if all((0 <= tmp[0] < self.map_size[0], 0 <= tmp[1] < self.map_size[1])):
                    self.map_list[tuple(origin + direction)] = self.floor
                    origin += direction
                else:
                    origin = np.asarray(self.start_point)
                    continue
            while self.map_list[self.start_point] != self.floor:
                self.set_start_point()
        self.set_player()
        self.set_lower_stairs()
        
    
    def map_save(self):
        self.map_init()
        self.create()
        np.savetxt('map.txt', self.map_list, fmt='%d')
