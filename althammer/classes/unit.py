class Unit(Base):

    def __repr__(self):
        return f"<Unit({self.faction.name} / {self.display_name})>"

    @property
    @cache.memoize()
    def permalink(self):
        return f"{self.faction.permalink}/unit/{self.id}"

    @lazy
    def ppm_computed(self):

        if self.profiles:

            ppm = sum([x.ppm_computed()*x.__dict__.get("qty",1) for x in self.profiles])
            if 'Entourage' not in self.core_rules:
                ppm /= sum([x.__dict__.get('qty',1) for x in self.profiles])
            return int(ppm)
            
            # hp = sum([x.hp for x in self.profiles])
            # save = self.profiles[0].save
            # tough = self.profiles[0].tough
            # invuln = self.profiles[0].__dict__.get('invuln', 7)
            # lead = self.profiles[0].lead
            # oc = self.profiles[0].oc
            # move = self.profiles[0].move
            # weapons=[]
            # for p in self.profiles:
            #     for w in p.default_weapons:
            #         weapons.append(w)
            # for w in self.default_weapons:
            #     weapons.append(w)
        else:
            hp=self.hp
            save=self.save
            tough=self.tough
            invuln=self.__dict__.get('invuln', 7)
            lead=self.lead
            oc=self.oc
            move=self.move
            weapons = self.default_weapons

        for x in self.core_rules:
            if not x.startswith('Feel No Pain'):
                continue
            fnp=int(x.split()[-1].rstrip('+'))
            break
        else:
            fnp=7
    

        if isinstance(move, str):
            move = int(move.rstrip('+'))

        defensive = hp * (6/(fnp-1)) * (6/(save-1)) * math.sqrt(tough) * math.sqrt(6/(invuln-1))
        
        if "Stealth" in self.keywords:
            defensive *= 1.2
        
        offensive = 0
        for weapon in weapons:
            offensive += weapon.weapon_points_raw

        if isinstance(move, str):
            move=int(move.rstrip('+'))
            
        strategic = (13-lead) + oc + move

        for kwd in self.core_rules:
            if kwd.startswith("Deadly Demise"):
                strategic *= 1.1
            elif kwd=="Deep Strike":
                strategic *= 1.3
            elif kwd=="Fights First":
                strategic *= 1.3
            elif kwd.startswith("Firing Deck"):
                strategic *= 1.5
            elif kwd=="Infiltrators":
                strategic *= 1.3
            elif kwd.startswith("Leader"):
                strategic *= 1.3
            elif kwd=="Lone Operative":
                strategic *= 1.2
            elif kwd=="Psyker":
                strategic *= 1.3
            elif kwd.startswith("Scouts"):
                strategic *= 1.1
            elif kwd=="Second in Command":
                strategic *= 1.1
            elif kwd=="Secured Objectives":
                strategic *= 2

        for kwd in self.keywords_all:
            if kwd=="Fly":
                strategic *= 1.1
            
        print(self.name, int(defensive), int(offensive), int(strategic))
        ppm = int((defensive * offensive * strategic)**(1/3))
        print(ppm)

        return ppm

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

        output = sorted(list(set(output)))
        return output

    @property
    def keywords_all(self):
        output = self.keywords
        if self.__dict__.get('profiles'):
            for profile in self.__dict__['profiles']:
                output += profile.get('keywords',[])

        return sorted(list(set(output)))

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
        return [
            Unit(
                x,
                faction=self.faction,
                display_name=f"{self.name} / Profile: {x['name']}",
                id=f"{self.id} / {x['name'].lower()}",
                is_profile=True,
                core_rules = self.core_rules
            ) for x in self.__dict__.get('profiles', [])]

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
