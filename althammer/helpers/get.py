from flask import abort
import json
import re
from werkzeug.utils import safe_join

from althammer.classes import *
from althammer.__main__ import app, cache

@cache.memoize()
def get_faction(faction):

    path=safe_join("althammer/data", faction)+"/faction.json"

    with open(path, "r+") as file:
        data=json.load(file)

    return Faction(data)

@cache.memoize()
def get_factions():

    path = "althammer/data/_factions.json"

    try:
        with open(path, "r+") as file:
            data=json.load(file)

    except FileNotFoundError:
        file_output = []

        root, dirs, files = next(os.walk(f"althammer/data/"))
        for directory in dirs:

            with open(f"althammer/data/{directory}/faction.json", "r+") as unitfile:
                try:
                    d=Faction(json.load(unitfile))
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(f"Unable to read detachment {self.id}/{filename}: {e}")
                file_output.append(
                    {
                        "id":d.id,
                        "name":d.name
                    }
                )

        with open(path, "w+") as f:
            f.write(json.dumps(file_output))

        return file_output



    return data

@cache.memoize()
def get_keyword(keyword):

    with open("althammer/data/keywords.json", "r+") as file:
        data=json.load(file)

    print(data)
    data = data['weapon_keywords']
    print(data)
    data.update(data['unit_keywords'])
    print(data)

    if keyword in data.keys():
        return keyword, data[keyword]

    elif keyword.startswith("Anti-"):
        return "Anti-Keyword X+", data["Anti-Keyword X+"]

    elif keyword.startswith("Leader"):
        return "Leader [Keyword]", data["Leader [Keyword]"]

    elif re.search(r"D?\d", keyword):
        keyword=re.sub(r"D?\d", "X", keyword)
        return keyword, data[keyword]

    else:
        return "Error", f"Unknown Keyword `{keyword}`"
