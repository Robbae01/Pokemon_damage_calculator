# Functions for getting move data

# Gets level up, tm and tr moves
def get_moves(move_dict, move_table):
    moves = move_table.find_all("tbody")[0].find_all("tr")
    for move in moves:
        move_info = {}
        move_data = move.find_all("td")
        if len(move_data) == 5:
            get_moves_short(move_dict, move_table, move_info, move_data)
        else:
            get_moves_long(move_dict, move_table, move_info, move_data)

def get_moves_long(move_dict, move_table, move_info, move_data):
    move_name = move_data[1].find("a").getText()

    move_type = move_data[2].find("a").getText()
    move_info["move_type"] = move_type

    move_category = move_data[3]["data-sort-value"]
    move_info["move_category"] = move_category

    move_power = move_data[4].getText()
    move_info["move_power"] = move_power

    move_accuracy = move_data[5].getText()
    move_info["move_accuracy"] = move_accuracy

    if move_name not in move_dict:
        move_dict[move_name] = move_info

# Gets egg, tutor and evolution moves
def get_moves_short(move_dict, move_table, move_info, move_data):
    move_name = move_data[0].find("a").getText()

    move_type = move_data[1].find("a").getText()
    move_info["move_type"] = move_type

    move_category = move_data[2]["data-sort-value"]
    move_info["move_category"] = move_category

    move_power = move_data[3].getText()
    move_info["move_power"] = move_power

    move_accuracy = move_data[4].getText()
    move_info["move_accuracy"] = move_accuracy

    if move_name not in move_dict:
        move_dict[move_name] = move_info