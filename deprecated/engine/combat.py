# Combat and initiative system placeholder

def roll_initiative(unit):
    from random import randint
    return unit.DEX + randint(1, 20)