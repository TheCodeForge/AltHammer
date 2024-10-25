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
        return f"<Unit({self.faction.name} / {self.display_name})>"

    @property
    def permalink(self):
        return f"{self.faction.permalink}/unit/{self.id}"

    @property
    def min_models(self):

        if self.__dict__.get('models_min'):
            return self.models_min
        elif any([x in self.keywords for x in ["Character","Monster","Vehicle","Epic Hero"]]):
            return 1

        else:
            return 0

    @property
    def max_models(self):

        print(f"max models for {self}")

        if self.__dict__.get('models_max'):
            max_unit_size= self.models_max
        elif any([x in self.keywords for x in ["Character","Monster","Vehicle","Epic Hero"]]):
            max_unit_size= 1

        elif self.profiles:
            for p in self.profiles:
                if any([x in p.keywords for x in ["Character","Monster","Vehicle","Epic Hero"]]):
                    max_unit_size=1

        else:
            max_unit_size = 100

        if "Battleline" in self.keywords:
            return max_unit_size * 6
        elif "Epic Hero" in self.keywords:
            return max_unit_size

        elif self.profiles:
            for p in self.profiles:
                if any([x in p.keywords for x in ["Epic Hero"]]):
                    return max_unit_size

        else:
            return max_unit_size * 3

    @property
    def profiles(self):
        return [Unit(x) for x in self.__dict__.get('profiles', [])]
    
    

    @property
    def display_name(self):
        if not self.__dict__.get("subtitle"):
            return self.name

        return f"{self.name} ({self.subtitle})"

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

        output = []

        root, dirs, files = next(os.walk(f"althammer/data/{self.id}/detachments"))
        for filename in files:
            with open(f"althammer/data/{self.id}/detachments/{filename}", "r+") as unitfile:
                try:
                    d=Detachment(json.load(unitfile))
                    d.id=filename.split('.')[0]
                    d.faction=self
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(f"Unable to read detachment {self.id}/{filename}: {e}")
                output.append(d)

        output = sorted(output, key= lambda x: x.name)

        return output
    
    @cache.memoize()
    def detachment(self, id):

        path = safe_join(f"althammer/data/{self.id}/detachments", f"{id}.json")

        try:
            with open(path, "r+") as file:
                data=json.load(file)
        except FileNotFoundError:
            abort(404)
        
        output = Detachment(data)

        output.faction=self
        return output

    @cache.memoize()
    def unit(self, id):

        path=safe_join(f"althammer/data/{self.id}/units", f"{id}.json")

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
    def units(self):

        output = {
            "Epic Hero": [],
            "Character": [],
            "Infantry": [],
            "Mounted": [],
            "Vehicle": [],
            "Monster": [],
            "Swarm": [],
            "Fortification": []
        }


        root, dirs, files = next(os.walk(f"althammer/data/{self.id}/units"))
        for filename in files:
            with open(f"althammer/data/{self.id}/units/{filename}", "r+") as unitfile:
                try:
                    u=Unit(json.load(unitfile))
                    u.id=filename.split('.')[0]
                    u.faction=self
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(f"Unable to read unit {self.id}/{filename}: {e}")
                for kind in output:
                    if kind in u.keywords:
                        output[kind].append(u)
                        break
                else:
                    raise ValueError(f"Unable to categorize unit {self.id}/{filename}")

        for kind in output:
            output[kind] = sorted(output[kind], key=lambda x: x.display_name)

        return output


    @property
    def color(self):
        return self.__dict__.get("color", "ADD8E6")
    
