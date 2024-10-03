from flask import abort
import json

from althammer.classes import *

def get_faction(faction):

    data = json.load(open("althammer/althammer/data/factions.json", "r+"))

    try:
        data=data[faction]
    except KeyError:
        abort(404)

    return Faction(data)

