# Unit data structure and stats
from ui.actors.actor import Actor


class Unit:
    def __init__(self, name, str_, dex, con, int_, wis, cha, actor: Actor):
        self.name = name
        self.STR = str_
        self.DEX = dex
        self.CON = con
        self.INT = int_
        self.WIS = wis
        self.CHA = cha
        self.HP = con * 20
        self.actor: Actor = actor

        self.initiative = 0
        self.armor_weight = 0
        self.weapon = None

    def __repr__(self):
        return f"{self.name} (HP: {self.HP})"