import json
import os
from werkzeug.utils import safe_join

from althammer.__main__ import cache

class Base():

    def __init__(self, data, *args, **kwargs):
        self.__dict__.update(data)
        self.__dict__.update(kwargs)

class Unit(Base):

    def __repr__(self):
        return f"<Unit({self.faction.name} / {self.name})>"

    @property
    @cache.memoize()
    def ranged_weapons(self):
        return [self.faction.weapon(x) for x in self.__dict__.get("range_weapons", [] )]

    @property
    @cache.memoize()
    def melee_weapons(self):
        if self.__dict__.get("melee_weapons"):
            return [self.faction.weapon(x) for x in self.__dict__.get("melee_weapons")]
        else:
            return [self.faction.default_melee_weapon]

    @property
    @cache.memoize()
    def wargear(self):
        if self.__dict__.get("wargear"):
            return [self.faction.weapon(x) for x in self.__dict__.get("wargear", [] )]
        else:
            return []
    

    @property
    def weapons(self):
        return self.ranged_weapons + self.melee_weapons + self.wargear
    

    @property
    @cache.memoize()
    def default_weapons(self):
        output = [self.faction.weapon(x) for x in self.__dict__["default_gear"]]
        if not self.__dict__.get('melee_weapons'):
            output.append(self.faction.default_melee_weapon)

        return output


    @property
    def faction_keywords(self):
        output = [self.faction.name]

        if self.__dict__.get('secondary_faction'):
            output.append(self.secondary_faction)

        return output

    def weapon(self, name):
        return self.faction.weapon(name)
    

class Weapon(Base):

    def __repr__(self):
        return f"<Weapon({self.faction.name} / {self.name})>"

class Detachment(Base):

    def __repr__(self):
        return f"<Detachment({self.faction.name} / {self.name})>"

    @property
    def permalink(self):
        return f"/faction/{self.faction.id}/detachment/{self.id}"


class Faction(Base):

    def __repr__(self):
        return f"<Faction({self.name})>"

    @property
    def permalink(self):
        return f"/faction/{self.id}"
    
    @property
    @cache.memoize()
    def detachments(self):

        path=f"althammer/data/{self.id}/_detachments.json"
        try:
            with open(path, "r+") as file:
                data=json.load(file)
        except Exception as e:
            print(e)
            return []
            
        output = [Detachment(x) for x in data.values()]

        for d in output:
            d.faction = self

        return output
    
    @cache.memoize()
    def detachment(self, id):

        for x in self.detachments:
            if x.id==id:
                output = x
                output.faction = self
                return output

        abort(404)

    @cache.memoize()
    def unit(self, id):

        path=safe_join(f"althammer/data/{self.id}/units", f"{id}.json")
        print(path)

        try:
            with open(path, "r+") as file:
                data=json.load(file)
        except FileNotFoundError:
            abort(404)
        
        output = Unit(data)

        output.faction=self
        return output

    @cache.memoize()
    def weapon(self, id):

        path=f"althammer/data/{self.id}/weapons/{id}.json"

        with open(path, "r+") as file:
            data=json.load(file)

        output = Weapon(data)
        output.faction=self
        return output

    @property
    @cache.memoize()
    def default_melee_weapon(self):
        return self.weapon("close_combat_weapon")

    
    @property
    @cache.memoize()
    def unit_listing(self):

        path=f"althammer/data/{self.id}/_units.json"

        try:
            with open(path, "r+") as file:
                data=json.load(file)

        except FileNotFoundError:

            file_output = {
                "Epic Hero": [],
                "Character": [],
                "Infantry": [],
                "Mounted": [],
                "Vehicle": [],
                "Swarm": [],
                "Fortification": []
            }

            for root, dirs, files in os.walk(f"althammer/data/{self.id}/units"):
                for filename in files:
                    with open(f"althammer/data/{self.id}/units/{filename}", "r+") as unitfile:
                        u=Unit(json.load(unitfile))
                        for kind in file_output:
                            if kind in u.keywords:
                                file_output[kind].append({
                                    "id":filename,
                                    "name":u.name
                                    })
                                break
                        else:
                            raise ValueError(f"Unable to categorize unit {self.id}/{filename}")

            with open (path, "w+") as f:
                f.write(json.dump(file_output))

            return file_output


        return data

    @property
    def color(self):
        return self.__dict__.get("color", "ADD8E6")
    