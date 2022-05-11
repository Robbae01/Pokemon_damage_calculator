import sys
import json

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import Counter

def handle_data(pokemon_list):
    counts = dict()
    for i in pokemon_list:
        counts[i] = counts.get(i, 0) + 1
    counts = dict(sorted(counts.items(), reverse=True, key=lambda item: item[1]))

    json_object = json.dumps(counts, indent=4)

    with open("pokemon_go_database.json", "a") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":

    all_pokemon = []
    open('pokemon_go_database.json', 'w').close()

    urls = ['https://silph.gg/t/w73h/results', 'https://silph.gg/t/8vp7/results']

    for url in urls:
        tournament = []
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

        player_rows = soup.find_all("table", {"class": "table table-condensed playerList text-left"})[0].find_all("tbody")[0].find_all("tr")
        for player in player_rows:
            player_data = player.find_all("td")
            pokemon_list = player_data[1].find_all("div", {"class": "pokemonEntry"})
            for pokemon in pokemon_list:
                final = pokemon.find_all("p")[1].getText()
                if pokemon.find("div", {"class": "shadowIcon"}):
                    final = "Shadow " + final
                tournament.append(final)
                all_pokemon.append(final)
        handle_data(tournament)
    handle_data(all_pokemon)
