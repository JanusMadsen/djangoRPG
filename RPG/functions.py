import random

def dice_roll(dice):
    return random.randint(1, dice)  # Simulate a dice roll

def resolve_turn(player, monster):
    if player.agility > monster.agility or dice_roll() > 10:
        return "player_turn"
    return "monster_turn"
