

def hp_calc(base_hp, iv, ev, level):
    hp = (((2 * base_hp) + iv + (ev / 4)) * level) / 100
    hp += (level + 10)
    hp = hp // 1
    return int(hp)

def stat_calc(base, iv, ev, level, nature, mod):
    stat = (((2 * base) + iv + (ev / 4)) * level) / 100
    stat += 5
    stat = stat * nature
    stat = stat // 1
    if mod < 0:
        stat = (stat * 2) / (2 + abs(mod))
    elif mod > 0:
        stat = (stat * (2 + abs(mod))) / 2
    return int(stat)
