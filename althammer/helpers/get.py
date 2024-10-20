from flask import abort
import json
import re

from althammer.classes import *
from althammer.__main__ import app, cache

@cache.memoize()
def get_faction(faction):

    with open("althammer/data/factions.json", "r+") as file:
        data=json.load(file)

    try:
        data=data[faction]
    except KeyError:
        abort(404)

    return Faction(data)

@cache.memoize()
def get_factions():

    with open("althammer/data/factions.json", "r+") as file:
        data=json.load(file)

    return sorted([Faction(x) for x in data.values()], key= lambda y: y.name)

@cache.memoize()
def get_keyword(keyword):

    with open("althammer/data/keywords.json", "r+") as file:
        data=json.load(file)

    if keyword in data.keys():
        return keyword, data[keyword]

    elif keyword.startswith("Anti-"):
        return "Anti-Keyword X+", data["Anti-Keyword X+"]

    elif re.search(r"\d", keyword):
        keyword=re.sub(r"\d", "X", keyword)
        return keyword, data[keyword]

    else:
        return "Error", f"Unknown Keyword `{keyword}`"
