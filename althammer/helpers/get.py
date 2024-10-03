import json

from .classes import *

def get_faction(faction):

    data = json.safe_load("althammer/althammer/data/factions.json")

    data=data[faction]

    return Faction(data)

