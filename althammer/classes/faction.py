import json
import os

from althammer.helpers.lazy import lazy

from .base import Base

from althammer.__main__ import cache

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

    @lazy
    def unit(self, id):

        path=safe_join(f"althammer/data/{self.id}/units", f"{id}.json")

        try:
            with open(path, "r+") as file:
                u = Unit(json.load(file))
                u.faction=self

                if 'id' not in u.__dict__:
                    # print(f'updating {filename}')
                    u.__dict__['id']=id
                    u.__dict__['ppm']=u.ppm_computed()
                    output = {x:u.__dict__[x] for x in u.__dict__}
                    output.pop('faction',None)
                    output.pop('_lazy',None)
                    file.seek(0)
                    file.write(json.dumps(output))
                    file.truncate()
                    
        except FileNotFoundError:
            abort(404)
            
        
        return u

    @lazy
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
    @lazy
    def unit_listing(self):

        cats = [
            "Epic Hero",
            "Character",
            "Infantry",
            "Mounted",
            "Vehicle",
            "Monster",
            "Swarm",
            "Fortification"
        ]

        categories = {x:[] for x in cats}


        root, dirs, files = next(os.walk(f"althammer/data/{self.id}/units"))
        for filename in files:
            with open(f"althammer/data/{self.id}/units/{filename}", "r+") as unitfile:
                # print(f"trying {filename}")
                try:
                    u=Unit(json.load(unitfile))
                    u.faction=self
                    # u.id=filename.split('.')[0]
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(f"Unable to read unit {self.id}/{filename}: {e}")

                # print(f'loaded {filename} to unit')

                # save id and points the first time a file is viewed
                if 'id' not in u.__dict__:
                    # print(f'updating {filename}')
                    u.id=filename.split('.')[0]
                    u.__dict__['ppm']=u.ppm_computed()
                    output = {x:u.__dict__[x] for x in u.__dict__}
                    output.pop('faction',None)
                    output.pop('_lazy', None)
                    unitfile.seek(0)
                    unitfile.write(json.dumps(output))
                    unitfile.truncate()
                    # print(f're-saved unit {u.display_name}')

            for kind in cats:
                # print(f"test {u.display_name} {u.keywords_all} for cat {kind}")
                if kind in u.keywords_all:
                    # print(f"Categorize {u.display_name} -> {kind}")
                    categories[kind].append(u)
                    break
            else:
                # print('cat error')
                raise ValueError(f"Unable to categorize unit {self.id}/{filename}")

            # print(f"Complete and going to next")

        categories = {kind:sorted(categories[kind], key=lambda x: x.display_name) for kind in categories}

        # print(categories)

        return categories


    @property
    def color(self):
        return self.__dict__.get("color", "000000")
