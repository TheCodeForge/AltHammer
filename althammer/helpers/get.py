from flask import abort
import json

from althammer.classes import *

def get_faction(faction):

    with open("althammer/data/factions.json", "r+") as file:
        data=json.load(file)

    try:
        data=data[faction]
    except KeyError:
        abort(404)

    return Faction(data)

def get_factions():

    with open("althammer/data/factions.json", "r+") as file:
        data=json.load(file)

    return sorted([Faction(x) for x in data.values()], key= lambda y: y.name)

    return Faction(data)