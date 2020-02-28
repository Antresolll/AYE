class Item:
    def __init__(self, st=0, damage=0, armor=0, hp=0, tile=None):
        self.st = st
        self.damage = damage
        self.armor = armor
        self.hp = hp

    def equip(self, persona):
        persona.damage += self.damage
        persona.armor += self.armor
        persona.st += self.st

    def reequip(self, persona):
        persona.damage -= self.damage
        persona.armor -= self.armor
        persona.st -= self.st

    def activate(self, persona):
        persona.hp += self.hp
        if persona.hp > persona.mx_hp:
            persona.hp = persona.mx_hp
