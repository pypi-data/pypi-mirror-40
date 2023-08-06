import json
import blackhc.notebook
import prettyprinter
import functools
import operator
import itertools

from implicit_lambda import call, contains
from teddy import *

with open("./data/swapi.json") as f:
    swapi = json.load(f)

swapi = teddy(swapi)

pprint = functools.partial(prettyprinter.pprint, max_seq_len=20)

pprint(sorted(swapi.people[:].name), max_seq_len=100, depth=4)

skywalker_films_urls = swapi.people.map_keys(_value["name"])[contains(_, "Skywalker")].films
pprint(skywalker_films_urls.result)

skywalker_films = swapi.films.map_keys(_value["url"])[skywalker_films_urls.result]
# pprint(skywalker_films.title.result)

# pprint(swapi, depth=1)
# pprint(swapi.films.map_keys(_value['url']), depth=2)

# TODO this is broken???
pprint(
    swapi.films.groupby("url")[skywalker_films_urls].map_values(lambda v: "").result, depth=5
)  # [skywalker_films_urls])
