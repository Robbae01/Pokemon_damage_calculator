import sys
import json


def weather_mod(weather, move, defender):
    if weather == 'None':
        return 1
    elif weather == 'Sunny':
        if move['move_type'] == 'Water':
            return 0.5
        if move['move_type'] == 'Fire':
            return 2
    elif weather == 'Rain':
        if move['move_type'] == 'Fire':
            return 0.5
        if move['move_type'] == 'Water':
            return 2
    elif weather == 'Sandstorm':
        if 'Rock' in defender['types'] and move['move_category'] == 'special':
            return 2 / 3
    elif weather == 'Hail':
        if move['move_type'] == 'Ice':
            return 2
    return 1

def terrain_mod(terrain, move, move_name):
    if terrain == 'None':
        return 1
    elif terrain == 'Grassy':
        if move['move_type'] == 'Grass':
            return 1.5
        elif move_name == 'Earthquake':
            return 0.5
    elif terrain == 'Misty':
        if move['move_type'] == 'Fairy':
            return 1.5
    elif terrain == 'Electric':
        if move['move_type'] == 'Electric':
            return 1.5
    elif terrain == 'Psychic':
        if move['move_type'] == 'Psychic':
            return 1.5
    return 1
        