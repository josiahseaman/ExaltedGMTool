from django.contrib.localflavor import us
from ElementTree import *
from DiceRoller import *
import json
import re


class TemporaryStat():
    def __init__(self, name, perm, temp=None):
        self.name = name
        self.permanent = perm
        self.temporary = self.permanent if temp is None else temp

    def __repr__(self):
        return self.name + ": " + str(self.temporary) + " of " + str(self.permanent)

    def __isub__(self, amount): # operator -=
        if self.temporary < amount:
            raise ValueError("You don't have enough " + self.name + " to do that.")
        self.temporary = self.temporary - amount
        print self.name, str(self.temporary), "remaining of", str(self.permanent)
        return self

    def __iadd__(self, amount):# operator +=
        self.temporary = min(self.temporary + amount, self.permanent)
        return self #TODO Add overflow check for Limit

    def __eq__(self, other):# operator ==
        try:
            return self.temporary == other.temporary
        except:
            return self.temporary == other


class VirtueChannel(TemporaryStat):
    def __isub__(self, other):
        TemporaryStat.__isub__(self, other)
        return self

    def __iadd__(self, other):
        TemporaryStat.__iadd__(self, other)
        return self

class HealthLevel(TemporaryStat):
    #TODO: this will need to eventually have 3 states: bashing, lethal, aggravated.  Apply Damage Push down rules
    """Characters have a list of health levels.  Once they run to the end of the list they are at least incapacitated.
    Along side this is a list of associated wound penalties.  Also damage stacking."""

    def __init__(self, name, perm, temp=None, penalties=[0,-1,-1,-2,-2,-4,-20]): #TODO: Handle incap being a string and dice penalty.
        TemporaryStat.__init__(self, name, perm, temp)
        self.penalties = []
        self.penalties = penalties

    def __isub__(self, other):
        TemporaryStat.__isub__(self, other)
        if self.temporary <= 0:
            raise ValueError()
        return self

    def empty(self):
        self.temporary = 0

    def woundPenalty(self):
        if self.temporary == self.permanent: return 0 # undamaged state
        return self.penalties[self.permanent - self.temporary - 1] # minus one because penalties[0] is for 1 damage

    def oxBody(self, purchases=1):
        for p in purchases:
            self.permanent += 3
            self.temporary += 3
            self.penalties.insert(self.penalties.index(-1), -1)
            self.penalties.insert(self.penalties.index(-2), -2)
            self.penalties.insert(self.penalties.index(-2), -2)

class ExaltedCharacter():
    def __init__(self, filename=None):
        self.name = "Unnamed"
        self.characterSheet = None
        if filename:
            filename = filename if '.ecg' in filename else filename + '.ecg'
            self.characterSheet = self.parseXML(filename)
            self.name = self.getName()
        self.virtues = ['Compassion', 'Conviction', 'Temperance', 'Valor']
        self.populateGearStats()
        '''Temporary Stats'''
        self.temporaryWillpower = self.newStat('Willpower')
        self.personalEssence = self.newStat('Personal Essence', self.calcPersonalEssence())
        self.peripheralEssence = self.newStat('Peripheral Essence', self.calcPeripheralEssence())
        self.health = HealthLevel('Health Levels', 7)
        self.isDying = False
        self.dyingHealthLevels = HealthLevel('Dying Health Levels', self["Stamina"])
        self.limit = self.newStat('Limit', 0, 10)
        self.CompassionChannel = self.newStat('Compassion')
        self.ConvictionChannel = self.newStat('Conviction')
        self.TemperanceChannel = self.newStat('Temperance')
        self.ValorChannel = self.newStat('Valor')
        self.dvPenalty = 0
        self.overrides = {}

    def __repr__(self):
        return "<" + self.name + ">"


    def newStat(self, name, valueOverride=None, maximum=None):
        '''Temporary State'''
        if valueOverride is None:
            return TemporaryStat(name, self[name])
        else:
            if maximum is None:
                return TemporaryStat(name, perm=valueOverride, temp=valueOverride)
            return TemporaryStat(name, perm=maximum, temp=valueOverride)

    '''Derived Stats'''

    def calcPersonalEssence(self): #This is only correct for Solars
        return self['Essence'] * 3 + self['Willpower']

    def calcPeripheralEssence(self): #This is only correct for Solars
        return self['Essence'] * 7 + self['Willpower'] + sum(
            self[x] for x in self.virtues) # - committed artifacts - permanent charms


    """Items Stats"""

    def createItemPath(self, itemName):
        if itemName is None:
            return None
        fileName = 'equipment/' + re.sub(r'[\W_]', '_', itemName) + '.item'
        try:
            with open(fileName): pass
        except IOError:
            print "Help! File name does not exist.", fileName
        return fileName

    def populateGearStats(self):
        gearList = self.gearList()
        self.armorStats = self.parseArmor(None)
        self.weaponStats = self.parseWeapon(None)
        gearList = self.handleSilkenArmor(gearList)
        for itemName in gearList:
            try:
                candidateA = self.parseArmor(itemName)
                if self.armorStats['lethalSoak'] < candidateA['lethalSoak']:
                    # print candidateA['name'], "wins over", self.armorStats['name'], '\n'
                    self.armorStats = candidateA
            except:
                try:
                    candidateW = self.parseWeapon(itemName)
                    if self.weaponStats['name'] == 'Punch' or self.weaponStats["damage"] < candidateW["damage"]:
                        # print candidateW['name'], "wins over", self.weaponStats['name'], '\n'
                        self.weaponStats = candidateW
                except: pass
        self.stackSilkenArmor()
        if self.armorStats['name'] == 'Unarmored':
            print self.name, "is missing Armor"
        if self.weaponStats['name'] == 'Punch':
            print self.name, "is missing Weapon"

    def gearList(self):
        models = self.additionalModels()
        gearNames = []
        for i in range(1, 20):  # try grabbing a gear name
            try:
                gearNames.append(models['Equipment'][0][i][0].itertext().next())
            except:
                pass
        return gearNames

    def additionalModels(self):
        e = self.characterSheet.getiterator('AdditionalModels').next()
        availableModels = {x.get('templateId'): x for x in e.getchildren()}
        return availableModels

    def parseArmor(self, itemName):
        filename = self.createItemPath(itemName)
        if filename is None:
            return {'name':'Unarmored', 'lethalSoak':0, 'bashingSoak':0, 'lethalHardness':0, 'bashingHardness':0, "fatigue":0, "mobilityPenalty":0, "attuneCost":0}
        stats = {}
        raw = json.load(open(filename))
        statBlock = raw["statsByRuleSet"]["SecondEdition"]
        stats['lethalSoak'] = statBlock[0]["soakByHealthType"]['Lethal']
        stats['bashingSoak'] = statBlock[0]["soakByHealthType"]['Bashing']
        stats['lethalHardness'] = statBlock[0]["hardnessByHealthType"]['Lethal']
        stats['bashingHardness'] = statBlock[0]["hardnessByHealthType"]['Bashing']
        stats["fatigue"] = statBlock[0]["fatigue"]
        stats["mobilityPenalty"] = statBlock[0]["mobilityPenalty"]
        try: stats["attuneCost"] = statBlock[1]["attuneCost"] # second statBlock only exists if it's an artifact
        except: pass
        stats['name'] = raw['name']
        return stats

    def parseWeapon(self, itemName):
        filename = self.createItemPath(itemName)
        if filename is None:
            return {"accuracy": 1, "damage": 0, "damageTypeString": "Bashing", "range": 5, "rate": 3, "speed": 5,
                    "defense": 2, "inflictsNoDamage": False, "tags": ['MartialArts'], "minimumDamage": 1,
                    "name": "Punch", "type": "Martial Arts"}
        raw = json.load(open(filename))
        stats = raw["statsByRuleSet"]["SecondEdition"][0]

        #Damage and attunement blocks are not strictly ordered.  Check for both in a list.
        for block in raw["statsByRuleSet"]["SecondEdition"]:
            if "damage" in block.keys():
                for key in block.keys():
                    stats[key] = block[key] #copies over all new keys
            stats["attuneCost"] = max(stats.get("attuneCost", 0), block.get("attuneCost", 0))
        if "damage" not in stats.keys():
            raise ValueError # this is so it fails if it's armor
        stats['name'] = raw['name']
        return stats

    def accuracy(self):
        weaponSkill = "Melee"
        mapping = {"Thrown":"Thrown", "BowType":"Archery", "MartialArts":"MartialArts"}
        for tag in self.weaponStats['tags']:
            if tag in mapping.keys():
                weaponSkill = mapping[tag]

        print "Using", weaponSkill
        total = self.sumDicePool('Dexterity', weaponSkill) + self.weaponStats['accuracy']
        return total

    def damageCode(self):
        return self.weaponStats['damage'] + self.sumDicePool('Strength', )

    def parryDV(self):  # Bows can lack the "defence" key
        return (self.weaponStats.get('defence',0) + self.sumDicePool('Dexterity', "Melee")) / 2

    def dodgeDV(self):
        return (self.sumDicePool('Dexterity', 'Dodge', 'Essence') + self.armorStats.get('mobilityPenalty',0) + self.health.woundPenalty()) / 2

    def DV(self):
        return max(0, max(self.parryDV(), self.dodgeDV()) + self.dvPenalty)

    def soak(self, damageType='lethal'):
        soakType = damageType + 'Soak'
        return self.sumDicePool('Stamina') / 2 + self.armorStats[soakType]

    def hardness(self, damageType='lethal'):
        hardnessType = damageType + 'Hardness'
        return self.armorStats[hardnessType]


    def parseXML(self, filename):
        """:return: Root node of the XML character sheet"""
        tree = ElementTree(file=filename)
        root = tree.getroot()
        return root

    def getName(self):
        return self.characterSheet.attrib['repositoryPrintName'].split()[0]

    def getStatNumber(self, element):
        result = element.get('experiencedValue', None)
        if not result:
            result = element.get('creationValue', None)
        return int(result or 0)

    def getStat(self, statName):
        statName = statName.lower().capitalize() #proper capitalization
        # try: return self.overrides[statName]
        # except: pass
        if statName == 'Martialarts': statName = 'MartialArts'
        try:
            element = self.characterSheet.getiterator(statName).next()
        except:
            return 0 #TODO: make this more clean than a silent failure
        if statName == 'Craft':
            branches = element.getiterator('subTrait')
            result = max(map(self.getStatNumber, branches))
        else:
            result = self.getStatNumber(element)
        #check for specialties, assumes they are applicable to this roll
        try:
            specialtyElem = element.iter('Specialty').next()
            print "Specialty:", specialtyElem.attrib['name'],
                 #currently I'm print this out to remind people of the assumption
            specialty = self.getStatNumber(specialtyElem)
        except:
            specialty = 0
        result += specialty
        return result

    def __getitem__(self, item):
        return self.getStat(item)

    def getText(self, elem):
        print elem
        return ",".join(elem.itertext())

    def sumDicePool(self, *stats):
        dicePool = 0
        for stat in stats: #I can do this with reduce, but it's harder to read
            try:
                dicePool += self[stat]
            except AttributeError:
                dicePool += stat #this is probably a number
        return max(0, dicePool - self.health.woundPenalty())

    def channelVirtue(self, virtue):
        attribName = virtue + 'Channel'
        self.__dict__[attribName] -= 1
        return self[virtue]


    def roll(self, *stats):
        """Each parameter is the name of a attribute, ability, or virtue.  It will automatically channel virtues.
        Any numbers that are placed will be counted as bonus dice.  Doesn't currently support auto-success beyond willpower.
        """
        stats = list(stats)#so that .remove() will work correctly (tuple is immutable)
        autoSuccesses = 0
        bonusDice = 0
        for trait in stats:
            if isinstance(trait, int):
                bonusDice += trait
                stats.remove(trait)
                continue
            if len(stats) > 1:
                if trait.lower() == 'willpower':
                    self.temporaryWillpower -= 1
                    autoSuccesses += 1
                    stats.remove(trait)#remove from list
                if trait in self.virtues:
                    self.temporaryWillpower -= 1 # even if this is a virtue channel it still takes 1wp
                    self.channelVirtue(trait) # mark off virtue channel
        label = reduce(lambda x,y: x+str(y)+" ", stats, '')
        rolledSuccesses = skillCheckByNumber(self.sumDicePool(*stats) + bonusDice, label)
        return rolledSuccesses + autoSuccesses

    def flurryAttack(self, nAttacks, defendingChar, hasPenalty=True):
        penalties = range( nAttacks-1, (nAttacks-1)+nAttacks) if hasPenalty else [0]*nAttacks
        for onslaught, penalty in enumerate(penalties):
            if defendingChar.isDying:
                print "Select a new target!", nAttacks-onslaught, "attacks left."
                return False
            damageDone = attackRoll(self.accuracy()-penalty, self.damageCode(), max(0, defendingChar.DV()-onslaught),
                                    defendingChar.soak(), defendingChar.hardness(), self.weaponStats.get('minimumDamage', 1))
            defendingChar.takeDamage(damageDone)
        return True

    def attack(self, defendingChar):
        damageDealt = attackRoll(self.accuracy(), self.damageCode(), defendingChar.DV(), defendingChar.soak(),
                                 defendingChar.hardness(), self.weaponStats.get('minimumDamage', 1))
        defendingChar.takeDamage(damageDealt)
        return damageDealt

    def takeDamage(self, damageDealt):
        try:
            self.health -= damageDealt
        except:
            self.health.empty()
            print self.name, "is dying"
            self.isDying = True

    def heal(self, healthGained):
        self.health += healthGained

    def joinBattle(self):
        return self.roll('Wits', 'Awareness')

    def stackSilkenArmor(self):
        #TODO: check for "Unarmored" and remove armorStats
        if self.isWearingSilkenArmor:
            properties = ['lethalSoak', 'bashingSoak', "fatigue", "mobilityPenalty", "attuneCost"] #hardness does not stack
            silkArmor = self.parseArmor('Silken Armor')
            for p in properties:
                self.armorStats[p] += silkArmor[p]
            self.armorStats['name'] += ' With Silken Armor'

    def handleSilkenArmor(self, gearList):
        assert isinstance(gearList, list)
        itemName = "Silken Armor"
        self.isWearingSilkenArmor = itemName in gearList
        if self.isWearingSilkenArmor:
            gearList.remove(itemName)
        return gearList

    def spend(self, amount):
        if self.peripheralEssence.temporary >= amount:
            self.peripheralEssence -= amount
        else:
            remainder = amount - self.peripheralEssence.temporary
            self.peripheralEssence -= self.peripheralEssence.temporary
            self.personalEssence -= remainder

    def regain(self, amount):
        room = self.personalEssence.permanent - self.personalEssence.temporary
        if room >= amount:
            self.peripheralEssence += amount
        else:
            remainder = amount - room
            self.personalEssence += room
            self.peripheralEssence += remainder

    def refreshDV(self):
        if self.isDying: # progress dying health levels,
            try:
                self.dyingHealthLevels -= 1
            except:
                print self.name, "is dead"
                raise ValueError, "Remove character from scene"
        else:
            self.dvPenalty = 0 # remove dv penalties
            # maintain grapple,
            self.regain(5) #TODO: regain motes (5 motes for meridians)



if __name__ == "__main__":
    print "ExaltedCharacter loaded"
