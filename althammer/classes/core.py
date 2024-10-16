import json
from werkzeug.utils import safe_join

from althammer.__main__ import cache

class Base():

    def __init__(self, data, *args, **kwargs):
        self.__dict__.update(data)
        self.__dict__.update(kwargs)

class Unit(Base):

    @property
    @cache.memoize()
    def ranged_weapons(self):
        return [self.faction.weapon(x) for x in self.__dict__["range_weapons"]]

    @property
    @cache.memoize()
    def melee_weapons(self):
        return [self.faction.weapon(x) for x in self.__dict__["melee_weapons"]]

    @property
    @cache.memoize()
    def default_weapons(self):
        return [self.faction.weapon(x) for x in self.__dict__["default_gear"]]

    def weapon(self, name):
        return self.faction.weapon(name)
    

class Weapon(Base):
    pass

class Detachment(Base):

    @property
    def permalink(self):
        return f"/faction/{self.faction.id}/detachment/{self.id}"


class Faction(Base):

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

        path=safe_join(f"althammer/data/{self.id}", f"{id}.json")
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

        path=f"althammer/data/{self.id}/_weapons.json"

        with open(path, "r+") as file:
            data=json.load(file)
        try:
            data=data[id]
        except KeyError:
            abort(404)

        output = Weapon(data)
        output.faction=self
        return output
    
    @cache.memoize()
    @property
    def unit_listing(self):

        path=f"althammer/data/{self.id}/_units.json"
        with open(path, "r+") as file:
            data=json.load(file)

        return data