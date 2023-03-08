from CustomImage import *


class Item:
    def __init__(self):
        self.name = 'Item'
        self.image = None
    
    def use(self):
        pass


class HealPotion10(Item):
    def __init__(self):
        super().__init__()
        self.name = '回復薬'
        self.image = PhotoImageHealPotion10()
        self.heal_point = 10
    
    def use(self, player):
        if player.hp + self.heal_point <= player.max_hp:
            player.hp += self.heal_point
        else:
            player.hp = player.max_hp
        return player


class HealPotion50(HealPotion10):
    def __init__(self):
        super().__init__()
        self.image = PhotoImageHealPotion50()
        self.heal_point = 50


class HealPotion100(HealPotion10):
    def __init__(self):
        super().__init__()
        self.image = PhotoImageHealPotion100()
        self.heal_point = 100
