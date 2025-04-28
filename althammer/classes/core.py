import json
import math
import os
from werkzeug.utils import safe_join

from flask import abort

from althammer.__main__ import cache

class Base():

    def __init__(self, data, *args, **kwargs):
        self.__dict__.update(data)
        self.__dict__.update(kwargs)

class Unit(Base):

    def __repr__(self):
        return f"<Unit({self.faction.name} / {self.display_name})>"

    @property
    @cache.memoize()
    def permalink(self):
        return f"{self.faction.permalink}/unit/{self.id}"

    @property
    @cache.memoize()
    def ppm(self):

        print(self.display_name)

        if self.profiles:
            hp = sum([x.hp for x in self.profiles])
            save = self.profiles[0].save
            tough = self.profiles[0].tough
            invuln = self.profiles[0].__dict__.get('invuln', 7)
            lead = self.profiles[0].lead
            oc = self.profiles[0].oc
            move = self.profiles[0].move
            weapons=[]
            for p in self.profiles:
                for w in p.default_weapons:
                    weapons.append(w)
            for w in self.default_weapons:
                weapons.append(w)
        else:
            hp=self.hp
            save=self.save
            tough=self.tough
            invuln=self.__dict__.get('invuln', 7)
            lead=self.lead
            oc=self.oc
            move=self.move
            weapons = self.default_weapons

        defensive = hp * (7-save) * math.sqrt(tough) * (8-invuln)
        if "Stealth" in self.keywords:
            defensive *= 1.17
        
        offensive = 0
        for weapon in weapons:
            if isinstance(weapon.dmg, str):
                dmg = eval(weapon.dmg.replace("d6", "3.5").replace("d3", "2"))
            else:
                dmg = weapon.dmg

            if isinstance(weapon.atk, str):
                atk = eval(weapon.atk.replace("d6", "3.5").replace("d3", "2"))
            else:
                atk = weapon.atk

            if "Torrent" in weapon.keywords:
                skl=1
            else:
                skl = weapon.skl

            rng = weapon.__dict__.get('rng',1)

            weapon_pts = (atk * (7-skl) * math.sqrt(weapon.str) * math.sqrt(weapon.ap+1) * dmg * math.sqrt(rng/12))

            # for kwd in weapon.keywords:
            #     if kwd=="Blast":
            #         weapon_pts*=1.2
            #     elif kwd=="Devastating Wounds":
            #         weapon_pts *= 1.2
            #     elif kwd=="Hazardous":
            #         weapon_pts *= 1 - (1/(6*hp))
            #     elif kwd=="Lethal Hits":
            #         weapon_pts *= 1.5
            #     elif kwd.startswith("Melta"):
            #         weapon_pts *= 1.5
            #     elif kwd=="One-Shot":
            #         weapon_pts /= 5
            #     elif kwd=="Rapid Fire":
            #         weapon_pts *= 1.5
            #     elif kwd.startswith("Sustained Hits"):
            #         weapon_pts *= 1.17
            #     elif kwd=="Twin-Linked":
            #         weapon_pts *= 1.25

            offensive += weapon_pts

        return offensive*defensive // 100

        strategic = (13-lead) * (1 + oc) * math.sqrt(move)

        for kwd in self.keywords:
            if kwd.startwith("Leader"):
                strategic *= 1.3
            if kwd=="Psyker":
                strategic *= 1.3
        
        total = offensive * defensive * strategic // 1000
        print(total)
        return total
                                                                       

    @property
    @cache.memoize()
    def min_models(self):

        if self.__dict__.get('models_min'):
            return self.models_min
        elif any([x in self.keywords for x in ["Character","Monster","Vehicle","Epic Hero"]]):
            return 1

        else:
            return 0

    @property
    @cache.memoize()
    def keywords(self):
        output = self.__dict__.get("keywords", [])

        if not self.__dict__.get('is_profile'):
            output += self.faction.__dict__.get("keywords", [])

        output = sorted(output)
        return output

    @property
    def keywords_all(self):
        output = self.keywords
        if self.profiles:
            for profile in self.profiles:
                output += profile.keywords

        return output

    @property
    @cache.memoize()
    def max_models(self):

        if self.__dict__.get('models_max'):
            max_unit_size = self.models_max
        elif any([x in self.keywords_all for x in ["Character","Monster","Vehicle","Epic Hero"]]):
            max_unit_size= 1

        else:
            max_unit_size = 100

        if "Battleline" in self.keywords_all:
            return max_unit_size * 6
        elif "Epic Hero" in self.keywords_all:
            return max_unit_size

        else:
            return max_unit_size * 3

    @property
    @cache.memoize()
    def profiles(self):
        return [Unit(x, faction=self.faction, display_name=f"{self.name} / Profile: {x['name']}", is_profile=True) for x in self.__dict__.get('profiles', [])]

    @property
    def display_name(self):

        if self.__dict__.get('display_name'):
            return self.__dict__['display_name']
            
        if not self.__dict__.get("subtitle"):
            return self.name

        return f"{self.name} ({self.subtitle})"

    @property
    @cache.memoize()
    def ranged_weapons(self):
        return sorted([self.faction.weapon(x) for x in self.__dict__.get("range_weapons", [] )], key=lambda x: x.name)

    @property
    @cache.memoize()
    def melee_weapons(self):
        if self.__dict__.get("melee_weapons"):
            return sorted([self.faction.weapon(x) for x in self.__dict__.get("melee_weapons")], key=lambda x: x.name)
        else:
            return [self.faction.default_melee_weapon]

    @property
    @cache.memoize()
    def wargear(self):
        if self.__dict__.get("wargear"):
            return sorted([self.faction.weapon(x) for x in self.__dict__.get("wargear", [] )], key=lambda x: x.name)
        else:
            return []
    
    @property
    def weapons(self):
        return self.ranged_weapons + self.melee_weapons + self.wargear
    
    @property
    @cache.memoize()
    def default_weapons(self):
        output = sorted([self.faction.weapon(x) for x in self.__dict__.get("default_gear",[])], key=lambda x: x.name)
        if not self.__dict__.get('melee_weapons') and not self.__dict__.get('is_profile'):
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
    
    @property
    def is_profile(self):
        return self.__dict__.get('is_profile', False)

class Weapon(Base):

    def __repr__(self):
        return f"<Weapon({self.faction.name} / {self.id})>"

    @property
    @cache.memoize()
    def profiles(self):
        return [Weapon(x, faction=self.faction, is_profile=True) for x in self.__dict__.get('profiles', [])]

    @property
    @cache.memoize()
    def keywords(self):
        return sorted(self.__dict__.get("keywords", []))

class Detachment(Base):

    def __repr__(self):
        return f"<Detachment({self.faction.name} / {self.name})>"

    @property
    def permalink(self):
        return f"/faction/{self.faction.id}/detachment/{self.id}"

    @cache.memoize()
    def is_legal(self, unit):

        if self.__dict__.get('secondary_faction') and unit.__dict__.get('secondary_faction') and self.secondary_faction != unit.secondary_faction:
            return False

        if any([x in unit.keywords for x in self.__dict__.get('banned_keywords', [])]):
            return False

        return True

    @property
    @cache.memoize()
    def unit_listing(self):
        #get faction unit listing and then filter by detachment rules
        unit_listing = self.faction.unit_listing

        output={x:[] for x in unit_listing}

        for cat in unit_listing:
            for unit in unit_listing[cat]:
                if not self.is_legal(unit):
                    continue

                output[cat].append(unit)

        return output

    @property
    @cache.memoize()
    def color(self):
        return self.__dict__.get('color', self.faction.color)

    @property
    @cache.memoize()
    def strategems(self):
        return self.faction.__dict__.get("strategems", []) + self.__dict__.get('strategems',[])
    
    @property
    @cache.memoize()
    def upgrades(self):

        return [Base(x, faction=self, id='_'.join(x['name'].lower().replace("'","").split())) for x in self.__dict__.get('upgrades', [])]
    
    

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
                    d=Detachment(json.load(unitfile), id=filename.split('.')[0])
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
        
        output = Detachment(data, id=id)


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
        
        output = Unit(data, id=id)

        output.faction=self
        return output

    @cache.memoize()
    def weapon(self, id):

        path=f"althammer/data/{self.id}/weapons/{id}.json"

        with open(path, "r+") as file:
            data=json.load(file)

        output = Weapon(data, id=id)
        output.faction=self
        return output

    @property
    @cache.memoize()
    def default_melee_weapon(self):
        return self.weapon("close_combat_weapon")

    
    @property
    @cache.memoize()
    def unit_listing(self):

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
                    if kind in u.keywords_all:
                        output[kind].append(u)
                        break
                else:
                    raise ValueError(f"Unable to categorize unit {self.id}/{filename}")

        for kind in output:
            output[kind] = sorted(output[kind], key=lambda x: x.display_name)

        return output


    @property
    def color(self):
        return self.__dict__.get("color", "000000")

    
