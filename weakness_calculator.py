import sys
import json

def weaknesses(attacking, defending):
    f = open('databases/type_chart.json')
    type_chart = json.load(f)

    multiplier = 1

    attacking_chart = next((x for x in type_chart if x["name"] == attacking), None)
    
    for def_type in defending:
        if def_type in attacking_chart["immunes"]:
            return 0
        if def_type in attacking_chart["weaknesses"]:
            multiplier = multiplier / 2
        if def_type in attacking_chart["strengths"]:
            multiplier = multiplier * 2

    return multiplier
    
