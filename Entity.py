import numpy as np
import random
from CustomImage import *


class Entity:
    def __init__(self):
        self.name = 'Entity'
        self.image = None
        self.dead_flg = False

        self.level = 0
        self.total_exp_required_level_up = 100
        self.total_exp_multiplier_required_level_up = 1.5
        self.total_exp = 0
        self.base_exp = 100

        self.physical_level = 0
        self.physical_name = '体力'
        self.physical_incremental = 10
        self.base_hp = 100
        self.hp_cache = None

        self.attack_level = 0
        self.attack_name = '攻撃力'
        self.attack_incremental = 1
        self.base_attack = 10

        self.defence_level = 0
        self.defence_name = '防御率'
        self.defence_incremental = 0.01
        self.base_defence = 10

        self.fortune_level = 0
        self.fortune_name = '運'
        self.fortune_incremental = 0.01
        self.base_fortune = 0.02

        self.status_list = [
            self.physical_name,
            self.attack_name,
            self.defence_name,
            self.fortune_name
        ]
    
    def status_update(self, hp_superscription=False):
        self.max_hp = self.base_hp
        self.max_hp += self.level * self.physical_incremental
        self.max_hp += self.physical_level * self.physical_incremental
        if hp_superscription:
            self.hp = self.max_hp
            self.hp_cache = self.hp

        self.attack = self.base_attack
        self.attack += self.attack_level * self.attack_incremental

        self.defence = self.base_defence
        self.defence_ratio = self.defence_level * self.defence_incremental

        self.fortune = self.base_fortune
        self.fortune += self.fortune_level * self.fortune_incremental

        self.exp = self.base_exp * (1 + self.level / 10)
    
    # 受けたダメージを反映
    def damaged(self, damage):
        self.hp_cache = self.hp
        self.hp -= damage
        # HPが0以下になった場合True
        if self.hp <= 0:
            self.hp = 0
            self.dead_flg = True


class EntityPlayer(Entity):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = PhotoImagePlayer
        self.items = np.empty(
            shape=(10,),
            dtype=object
        )
        self.status_update(hp_superscription=True)
    
    def level_up(self):
        self.level += 1
        self.total_exp_required_level_up *= \
            self.total_exp_multiplier_required_level_up
        
        self.physical_level = self.level
        self.attack_level = self.level
        self.defence_level = self.level
        self.fortune_level = self.level

        self.status_update()

    def add_exp(self, exp):
        self.total_exp += exp
        while self.total_exp >= self.total_exp_required_level_up:
            self.level_up()


class EntityEnemy(Entity):
    def __init__(self):
        super().__init__()
        self.status_weights = [
            0.25,   # physical
            0.25,   # attack
            0.25,   # defence
            0.25,   # fortune
        ]
    
    def set_random_status_level(self):
        for _ in range(self.level):
            status = random.choices(
                self.status_list,
                weights=self.status_weights,
                k=1
            )[0]
            match status:
                case self.physical_name:
                    self.physical_level += 1
                case self.attack_name:
                    self.attack_level += 1
                case self.defence_name:
                    self.defence_level += 1
                case self.fortune_name:
                    self.fortune_level += 1
        self.status_update(hp_superscription=True)


class EntitySlimePattern1(EntityEnemy):
    def __init__(self, name, level=0):
        super().__init__()
        self.name = name
        self.image = PhotoImageSlimePattern1()
        self.level = level
        self.physical_incremental *= 2
        self.status_weights = [
            0.7,   # physical
            0.1,   # attack
            0.1,   # defence
            0.1,   # fortune
        ]
        self.set_random_status_level()


class EntitySlimePattern2(EntityEnemy):
    def __init__(self, name, level=0):
        super().__init__()
        self.name = name
        self.image = PhotoImageSlimePattern2()
        self.level = level
        self.attack_incremental *= 2
        self.status_weights = [
            0.1,   # physical
            0.7,   # attack
            0.1,   # defence
            0.1,   # fortune
        ]
        self.set_random_status_level()


class EntitySlimePattern3(EntityEnemy):
    def __init__(self, name, level=0):
        super().__init__()
        self.name = name
        self.image = PhotoImageSlimePattern3()
        self.level = level
        self.defence_incremental *= 2
        self.status_weights = [
            0.1,   # physical
            0.1,   # attack
            0.7,   # defence
            0.1,   # fortune
        ]
        self.set_random_status_level()


class EntitySlimePattern4(EntityEnemy):
    def __init__(self, name, level=0):
        super().__init__()
        self.name = name
        self.image = PhotoImageSlimePattern4()
        self.level = level
        self.fortune_incremental *= 2
        self.status_weights = [
            0.1,   # physical
            0.1,   # attack
            0.1,   # defence
            0.7,   # fortune
        ]
        self.set_random_status_level()
