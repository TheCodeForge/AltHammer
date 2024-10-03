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

def get_detachment(faction, detachment):

    f=get_faction(faction)

    with open(f"althammer/data/{f.id}/_detachments.json", "r+") as file:
        data=json.load(file)

    try:
        data=data[detachment]
    except KeyError:
        abort(404)

    return Detachment(data)