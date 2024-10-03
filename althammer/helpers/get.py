from flask import abort
import json

from althammer.classes import *

def get_faction(faction):

    with open("althammer/data/factions.json", "r+") as f:
        data=json.load(f)

    try:
        data=data[faction]
    except KeyError:
        abort(404)

    return Faction(data)

