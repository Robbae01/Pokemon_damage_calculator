import sys
import json

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from move_functions import *

# Which games in the series are being used
SS = 18
POKEMON_GAME = SS



if __name__ == "__main__":

    all_moves= {}
    open('../databases/move_database.json', 'w').close()

    url = 'https://pokemondb.net/move/all'
    request = Request(
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
    )

    page = urlopen(request)
    page_content_bytes = page.read()
    page_html = page_content_bytes.decode("utf-8")

    soup = BeautifulSoup(page_html, "html.parser")

    move_rows = soup.find_all("table", id="moves")[0].find_all("tbody")[0].find_all("tr")
    for move in move_rows:
        move_contents = {}
        move_data = move.find_all("td")
        move_name = move_data[0].find_all("a")[0].getText()
        type_is = move_data[1].find_all("a")
        
        if type_is:
            move_type = type_is[0].getText()
        else:
            move_type = "typeless"

        move_contents["move_type"] = move_type

        move_category = move_data[2]["data-sort-value"]
        move_contents["move_category"] = move_category

        move_power = move_data[3].getText()
        if move_power == '\u2014':
            move_power = '-'
        move_contents["move_power"] = move_power

        all_moves[move_name] = move_contents


    json_object = json.dumps(all_moves, indent=4)

    with open("../databases/move_database.json", "a") as outfile:
        outfile.write(json_object)
        