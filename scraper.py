import sys
import json

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from move_functions import *

# Which games in the series are being used
SS = 18
POKEMON_GAME = SS



if __name__ == "__main__":

    all_pokemon = {}
    open('pokemon_database.json', 'w').close()

    url = 'https://pokemondb.net/pokedex/all'
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

    pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")
    for pokemon in pokemon_rows:
        pokemon_contents = {}
        pokemon_data = pokemon.find_all("td")
        id = pokemon_data[0]["data-sort-value"]
        pokemon_contents["pokedex_no"] = id
        
        name = pokemon_data[1].find_all("a")[0].getText()
        forme = ""
        if pokemon_data[1].find_all("small"):
            forme = pokemon_data[1].find_all("small")[0].getText()
        pokemon_contents["forme"] = forme
        if name in forme:
            name = forme
        elif forme:
            name = f'{name} {forme}'
        print(name)
        
        detail_url = pokemon_data[1].find_all("a")[0]["href"]

        typing = []
        for pokemon_type in pokemon_data[2].find_all("a"):
            typing.append(pokemon_type.getText())
        pokemon_contents["types"] = typing

        # Retrieve the base stats
        total = pokemon_data[3].getText()
        hp = pokemon_data[4].getText()
        attack = pokemon_data[5].getText()
        defence = pokemon_data[6].getText()
        sp_attack = pokemon_data[7].getText()
        sp_defence = pokemon_data[8].getText()
        speed = pokemon_data[9].getText()

        pokemon_contents["bs_total"] = total
        pokemon_contents["hp"] = hp
        pokemon_contents["attack"] = attack
        pokemon_contents["defence"] = defence
        pokemon_contents["sp_attack"] = sp_attack
        pokemon_contents["sp_defence"] = sp_defence
        pokemon_contents["speed"] = speed

        # Get the details for a specific pokemon
        pokemon_url = f'https://pokemondb.net{detail_url}'
        pokemon_request = Request(
            pokemon_url,
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
        )
        pokemon_page = urlopen(pokemon_request)
        pokemon_page_content_bytes = pokemon_page.read()
        pokemon_page_html = pokemon_page_content_bytes.decode("utf-8")

        # Get the abilities of a specific pokemon
        pokemon_soup = BeautifulSoup(pokemon_page_html, "html.parser")
        abilities_row = pokemon_soup.find_all("main")[0].find_all("table")[0].find_all("tr")[5]
        pokemon_data = abilities_row.find_all("td")[0]
        pokemon_abilities = pokemon_data.find_all("a")
        abilities = []
        for ability in pokemon_abilities:
            ability_name = ability.getText()
            abilities.append(ability_name)
        pokemon_contents["abilities"] = abilities
        
        # Get the pokemons moves
        all_moves = pokemon_soup.find("div", id=f'tab-moves-{POKEMON_GAME}')
        if all_moves is None:
            continue
        all_move_tables = all_moves.find_all("table")

        moves = {}

        for move_table in all_move_tables:
            get_moves(moves, move_table)
        

        pokemon_contents["moves"] = moves

        all_pokemon[name] = pokemon_contents

    json_object = json.dumps(all_pokemon, indent=4)

    with open("pokemon_database.json", "a") as outfile:
        outfile.write(json_object)
        