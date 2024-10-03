import json

class Base():

    def __init__(self, data):
        self.__dict__.update(data)

class Detachment(Base):
    pass


class Faction(Base):
    
    @property
    def detachments(self):

        with open(f"althammer/data/{self.id}/_detachments.json", "r+") as file:
            data=json.load(file)

        return [Detachment(x) for x in data.values()]
    
    def detachment(self, id):

        for x in self.detachments:
            if x.id==id:
                return x

        abort(404)