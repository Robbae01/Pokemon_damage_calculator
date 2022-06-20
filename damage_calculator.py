import sys
import json

from math import floor, trunc
from weakness_calculator import weaknesses
from stat_calculation import *
from helper_functions import *
from field_conditions import *

def main():

    f = open('databases/pokemon_database.json')
    database = json.load(f)

    f = open('databases/move_database.json')
    moves = json.load(f)

    # Get the data for the attacker
    attacker_name = "Groudon"
    attacker = get_pokemon(attacker_name, database)
    attacker_nature = "Adamant"
    attacker_evs = {
        'hp': 0,
        'atk': 252,
        'def': 0,
        'sp_atk': 0,
        'sp_def': 0,
        'spd': 252
    }
    attacker_ivs = {
        'hp': 31,
        
        'atk': 31,
        'def': 31,
        'sp_atk': 31,
        'sp_def': 31,
        'spd': 31
    }
    attacker_mods = {
        'hp': 0,
        'atk': -1,
        'def': 0,
        'sp_atk': 0,
        'sp_def': 0,
        'spd': 0
    }

    # Get the data for the defender
    defender_name = "Incineroar"
    defender = get_pokemon(defender_name, database)
    defender_nature = "Impish"
    defender_evs = {
        'hp': 252,
        'atk': 0,
        'def': 28,
        'sp_atk': 0,
        'sp_def': 156,
        'spd': 0
    }
    defender_ivs = {
        'hp': 31,
        'atk': 31,
        'def': 31,
        'sp_atk': 31,
        'sp_def': 31,
        'spd': 31
    }
    defender_mods = {
        'hp': 0,
        'atk': 0,
        'def': 0,
        'sp_atk': 0,
        'sp_def': 0,
        'spd': 0
    }
    

    # Get the data for the attack
    move_name = "Precipice Blades"
    move = get_move(move_name, moves)

    # Get the field conditions
    weather_condition = 'None'
    terrain = 'None'

    f = open('databases/natures.json')
    natures = json.load(f)

    print(natures[attacker_nature])
    print(natures[defender_nature])

    # get the stat modifiers for the natures
    atk_nature = natures[attacker_nature]
    def_nature = natures[defender_nature]
    atk_mod = nature_mod(atk_nature, "attack")
    def_mod = nature_mod(def_nature, "defence")
    sp_atk_mod = nature_mod(atk_nature, "special attack")
    sp_def_mod = nature_mod(def_nature, "special defence")
    level = 50
    attack_category = ""
    defence_category = ""


    hp = hp_calc(int(defender["hp"]), defender_ivs['hp'], defender_evs['hp'], level)
    if move["move_category"] == "special":
        attack = stat_calc(int(attacker["sp_attack"]), attacker_ivs['sp_atk'], attacker_evs['sp_atk'], level, sp_atk_mod, attacker_mods['sp_atk'])
        defence = stat_calc(int(defender["sp_defence"]), defender_ivs['sp_def'], defender_evs['sp_def'], level, sp_def_mod, defender_mods['sp_def'])
        attack_category = "SpA"
        defence_category = "SpD"
    elif move["move_category"] == "physical":
        attack = stat_calc(int(attacker["attack"]), attacker_ivs['atk'], attacker_evs['atk'], level, atk_mod, attacker_mods['atk'])
        defence = stat_calc(int(defender["defence"]), defender_ivs['def'], defender_evs['def'], level, def_mod, defender_mods['def'])
        attack_category = "Atk"
        defence_category = "Def"
    else:
        print("This is a status move")

    power = move["move_power"]
    attack_type = move["move_type"]
    defender_type = defender["types"]
    power = int(move["move_power"])
    targets = 1
    weather = weather_mod(weather_condition, move, defender)
    crit = False
    crit_dmg = 1
    if crit:
        crit_dmg = 1.5
    rand_high = 1
    rand_low = 0.85
    stab = 1
    if move["move_type"] in attacker["types"]:
        stab = 1.5
    type_dmg = weaknesses(attack_type, defender_type)
    burn = 1
    burned = False
    if move["move_category"] == "physical" and burned == True:
        burn = 0.5
    other = terrain_mod(terrain, move, move_name)

    # Oreder of multiplication: targets * weather * crit * random * stab * type * burn * other
    # Calculate the damage done
    base_damage = (floor((2 * level // 5 + 2) * power * attack / defence) // 50 + 2)

    print(base_damage, targets, weather, crit_dmg, rand_high, stab, type_dmg, burn, other)

    max_damage = final_damage(base_damage, targets, weather, crit_dmg, rand_high, stab, type_dmg, burn, other)
    min_damage = final_damage(base_damage, targets, weather, crit_dmg, rand_low, stab, type_dmg, burn, other)

    max_percentage = truncate(((max_damage / hp) * 100), 1)
    min_percentage = truncate(((min_damage / hp) * 100), 1)

    hp_ev = defender_evs['hp']
    atk_ev = 0
    def_ev = 0
    if move['move_category'] == 'physical':
        atk_ev = attacker_evs['atk']
        def_ev = defender_evs['def']
    elif move['move_category'] == 'special':
        atk_ev = attacker_evs['sp_atk']
        def_ev = defender_evs['sp_def']
    #output to be shown to the user
    output = f'{atk_ev}+ {attack_category} {attacker_name} {move_name} vs. {hp_ev} HP / {def_ev} {defence_category} {defender_name} -- {min_percentage}% - {max_percentage}% '
    print(output)

# Functions solely for this program
def get_pokemon(name, database):
        return database[name]

def get_move(name, moves):
    move = moves[name]
    return move

def nature_mod(nature, stat):
    if nature["raises"] == stat:
        return 1.1
    elif nature["lowers"] == stat:
        return 0.9
    return 1

def final_damage(damage, *multipliers):
    for multiplier in multipliers:
        damage = floor(damage * multiplier)
    return damage

if __name__ == "__main__":
    main()