import json

class Base():

    def __init__(self, data):
        self.__dict__.update(data)

class Detachment(Base):

    @property
    def permalink(self):
        return f"/faction/{self.faction.id}/detachment/{self.id}"


class Faction(Base):
    
    @property
    def detachments(self):

        with open(f"althammer/data/{self.id}/_detachments.json", "r+") as file:
            data=json.load(file)

        output = [Detachment(x) for x in data.values()]

        for d in output:
            d.faction = self

        return output
    
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
    