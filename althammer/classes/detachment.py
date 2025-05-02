from althammer.helpers.lazy import lazy

from .base import Base

from althammer.__main__ import cache

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
    @lazy
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