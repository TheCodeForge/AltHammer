import json

from althammer.__main__ import cache

class Base():

    def __init__(self, data):
        self.__dict__.update(data)

class Detachment(Base):

    @property
    def permalink(self):
        return f"/faction/{self.faction.id}/detachment/{self.id}"


class Faction(Base):
    
    @property
    @cache.memoize()
    def detachments(self):

        try:
            with open(f"althammer/data/{self.id}/_detachments.json", "r+") as file:
                data=json.load(file)
        except:
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

    @property
    def permalink(self):
        return f"/faction/{self.id}"
    