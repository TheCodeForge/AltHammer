from flask import abort
import json

from .classes import *

def get_faction(faction):

    data = json.safe_load("althammer/althammer/data/factions.json")

    try:
        data=data[faction]
    except KeyError:
        abort(404)
        
    return Faction(data)

