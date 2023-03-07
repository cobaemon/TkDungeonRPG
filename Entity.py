import numpy as np


class Entity:
    def __init__(self):
        self.entity_name = 'Entity'
        self.entity_hp = 100
        self.entity_max_hp = 100
        self.entity_attack_point = 10


class EntityPlayer(Entity):
    def __init__(self, entity_name):
        super().__init__()
        self.entity_name = entity_name
        self.items = np.empty(
            shape=(10,),
            dtype=object
        )
