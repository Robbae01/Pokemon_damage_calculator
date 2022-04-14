import sys
import json

from math import floor, trunc
from weakness_calculator import weaknesses
from stat_calculation import *
from helper_functions import *

def main():

    f = open('pokemon_database.json')
    database = json.load(f)

    attacker_name = "Kyogre"
    defender_name = "Kyogre"
    move_name = "Water Spout"
    attacker_nature = "Adamant"
    defender_nature = "Jolly"

    attacker = get_pokemon(attacker_name, database)
    defender = get_pokemon(defender_name, database)
    move = get_move(move_name, attacker)

    f = open('natures.json')
    natures = json.load(f)

    atk_nature = natures[attacker_nature]
    def_nature = natures[defender_nature]
    atk_mod = nature_mod(atk_nature, "attack")
    def_mod = nature_mod(atk_nature, "defence")
    sp_atk_mod = nature_mod(atk_nature, "special attack")
    sp_def_mod = nature_mod(atk_nature, "special defence")
    level = 100
    attack = 0
    defence = 200
    sp_attack = 0
    sp_defence = 0
    atk_ev = 252
    def_ev = 0
    hp_ev = 252
    attack_category = ""
    defence_category = ""


    hp = hp_calc(int(defender["hp"]), 31, hp_ev, level)
    if move["move_category"] == "special":
        attack = stat_calc(int(attacker["sp_attack"]), 31, atk_ev, level, sp_atk_mod)
        defence = stat_calc(int(defender["sp_defence"]), 31, def_ev, level, sp_def_mod)
        attack_category = "SpA"
        defence_category = "SpD"
    elif move["move_category"] == "physical":
        attack = stat_calc(int(attacker["attack"]), 31, atk_ev, level, atk_mod)
        defence = stat_calc(int(defender["defence"]), 31, def_ev, level, def_mod)
        attack_category = "Atk"
        defence_category = "Def"
    else:
        print("This is a status move")

    power = move["move_power"]
    attack_type = move["move_type"]
    defender_type = defender["types"]
    power = int(move["move_power"])
    targets = 1
    weather = 1
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
    other = 1

    print(f'level: {level}')
    print(f'attack power: {power}')
    print(f'attack stat: {attack}')
    print(f'defence: {defence}')
    print(f'type effectiveness: {type_dmg}')
    print(f'stab: {stab}')

    # Oreder of multiplication: targets * weather * crit * random * stab * type * burn * other
    # Calculate the damage done
    base_damage = (floor((2 * level // 5 + 2) * power * attack / defence) // 50 + 2)

    max_damage = final_damage(base_damage, targets, weather, crit_dmg, rand_high, stab, type_dmg, burn, other)
    min_damage = final_damage(base_damage, targets, weather, crit_dmg, rand_low, stab, type_dmg, burn, other)

    max_percentage = truncate(((max_damage / hp) * 100), 1)
    min_percentage = truncate(((min_damage / hp) * 100), 1)

    #output to be shown to the user
    output = f'{atk_ev}+ {attack_category} {attacker_name} {move_name} vs. {hp_ev} HP / {def_ev} {defence_category} {defender_name} -- {min_percentage}% - {max_percentage}% '
    print(output)

# Functions solely for this program
def get_pokemon(name, database):
        return database[name]

def get_move(name, pokemon):
    moves = pokemon["moves"][name]
    return moves

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