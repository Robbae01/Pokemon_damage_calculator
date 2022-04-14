

def hp_calc(base_hp, iv, ev, level):
    hp = (((2 * base_hp) + iv + (ev / 4)) * level) / 100
    hp += (level + 10)
    hp = hp // 1
    return int(hp)

def stat_calc(base, iv, ev, level, nature):
    stat = (((2 * base) + iv + (ev / 4)) * level) / 100
    stat += 5
    stat = stat * nature
    stat = stat // 1
    return int(stat)

hp = hp_calc(80, 31, 154, 100)
attack = stat_calc(82, 31, 252, 100, 1)
print(hp)
print(attack)