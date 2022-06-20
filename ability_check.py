import sys
import json


def ability_check(attacker, defender, move):
    if (attacker[ability] == 'Fairy Aura' or defender[ability] == 'Fairy Aura') and move['move_type'] == 'Fairy':
        return 1.5
    if (attacker[ability] == 'Dark Aura' or defender[ability] == 'Dark Aura') and move['move_type'] == 'Dark':
        return 1.5
    
def terrain_ability(attacker, defender):
    