import numpy as np


class Entity:
    def __init__(self):
        self.name = 'Entity'
        self.hp = 100
        self.hp_cache = self.hp
        self.max_hp = 100
        self.attack_point = 10


class EntityPlayer(Entity):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.items = np.empty(
            shape=(10,),
            dtype=object
        )
