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

    def __isub__(self, amount):
        if self.temporary < amount:
            raise ValueError("You don't have enough " + self.name + " to do that.")
        self.temporary = self.temporary - amount
        print self.name, str(self.temporary), "remaining of", str(self.permanent)
        return self

    def __iadd__(self, amount):
        self.temporary = min(self.temporary + amount, self.permanent)
        return self

    def __eq__(self, other):
        try:
            return self.temporary == other.temporary
        except:
            return self.temporary == other


class VirtueChannel(TemporaryStat):
    def __isub__(self, other):
        super.__isub__(self, other)
        return self.permanent

    def __iadd__(self, other):
        super.__iadd__(self, other)
        return self.permanent


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
        self.wounds = self.newStat('Wounds', 0, 7)
        self.limit = self.newStat('Limit', 0, 10)
        self.CompassionChannel = self.newStat('Compassion')
        self.ConvictionChannel = self.newStat('Conviction')
        self.TemperanceChannel = self.newStat('Temperance')
        self.ValorChannel = self.newStat('Valor')
        # self.virtueChannel =

    def __repr__(self):
        return "Character: " + self.name

    '''Temporary State'''

    def newStat(self, name, valueOverride=None, maximum=None):
        if valueOverride is None:
            return TemporaryStat(name, self.getStat(name))
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
    def populateGearStats(self):
        gearList = self.gearList()
        self.armorStats = self.parseArmor(None)
        self.weaponStats = self.parseWeapon(None)
        for itemName in gearList:
            fileName = 'equipment/' + re.sub(r'[\W_]', '_', itemName) + '.item'
            try:
                with open(fileName): pass
            except IOError:
                print "Help! File name does not exist.", fileName
            try:
                candidateA = self.parseArmor(fileName)
                if self.armorStats['lethalSoak'] < candidateA['lethalSoak']:
                    print candidateA['name'], "wins over", self.armorStats['name'], '\n'
                    self.armorStats = candidateA
            except:
                try:
                    candidateW = self.parseWeapon(fileName)
                    if self.weaponStats['name'] == 'Punch' or self.weaponStats["damage"] < candidateW["damage"]:
                        print candidateW['name'], "wins over", self.weaponStats['name'], '\n'
                        self.weaponStats = candidateW
                except: pass

        if not self.armorStats:
            print self.name, "is missing Armor"
            self.armorStats = self.parseArmor(None)
        if not self.weaponStats:
            print self.name, "is missing Weapon"
            self.weaponStats = self.parseWeapon(None)

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

    def parseArmor(self, filename):
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
        stats["attuneCost"] = statBlock[1]["attuneCost"]
        stats['name'] = raw['name']
        return stats

    def parseWeapon(self, filename):
        if filename is None:
            return {"accuracy": 1, "damage": 0, "damageTypeString": "Bashing", "range": 5, "rate": 3, "speed": 5,
                    "defense": 2, "inflictsNoDamage": False, "tags": [], "minimumDamage": 1, "name": "Punch", "type": "Martial Arts"}
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
        try:
            total = self.sumDicePool('Dexterity', "Melee") + self.weaponStats['accuracy']
            return total
        except:
            return self.sumDicePool('Dexterity', "Melee")

    def damageCode(self):
        return self.weaponStats['damage'] + self.sumDicePool('Strength', )

    def parryDV(self):  # Bows can lack the "defence" key
        return (self.weaponStats.get('defence',0) + self.sumDicePool('Dexterity', "Melee")) / 2

    def dodgeDV(self):
        return (self.sumDicePool('Dexterity', 'Dodge', 'Essence') - self.armorStats.get('mobilityPenalty',0)) / 2

    def DV(self):
        return max(self.parryDV(), self.dodgeDV())

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
        return self.characterSheet.attrib['repositoryPrintName']

    def getStatNumber(self, element):
        result = element.get('experiencedValue', None)
        if not result:
            result = element.get('creationValue', None)
        return int(result or 0)

    def getStat(self, statName):
        statName = statName.lower().capitalize() #proper capitalization
        try:
            element = self.characterSheet.getiterator(statName).next()
        except:
            return 0
        result = self.getStatNumber(element)
        #check for specialties, assumes they are applicable to this roll
        try:
            specialtyElem = element.iter('Specialty').next()
            print "Specialty:", specialtyElem.attrib[
                'name'], #currently I'm print this out to remind people of the assumption
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
            dicePool += self[stat]
        return dicePool #- self.woundPenalty

    def channelVirtue(self, virtue):
        attribName = virtue + 'Channel'
        self.__dict__[attribName] -= 1
        return self[virtue]


    """Each parameter is the name of a attribute, ability, or virtue.  It will automatically channel virtues.
    Any numbers that are placed will be counted as bonus dice.  Doesn't currently support auto-success beyond willpower.
    """
    def roll(self, *stats):
        stats = list(stats)#so that .remove() will work correctly (tuple is immutable)
        autoSuccesses = 0
        bonusDice = 0
        for trait in stats:
            if isinstance(trait, int):
                bonusDice += trait
                stats.remove(trait)
                continue
            if len(stats) > 1:
                if (trait.lower() == 'willpower'):
                    self.temporaryWillpower -= 1
                    autoSuccesses += 1
                    stats.remove(trait)#remove from list
                if trait in self.virtues:
                    self.temporaryWillpower -= 1#even if this is a virtue channel it still takes 1wp
                    self.channelVirtue(trait)#mark off virtue channel

        rolledSuccesses = skillCheckByNumber(self.sumDicePool(*stats) + bonusDice)
        return rolledSuccesses + autoSuccesses

    def flurryAttack(self, nAttacks, defendingChar):
        return flurry(nAttacks, self.accuracy(), self.damageCode(), defendingChar.DV(), defendingChar.soak(),
                      defendingChar.hardness())

    def joinBattle(self):
        return self.roll('Wits', 'Awareness')


if __name__ == "__main__":
    print "ExaltedCharacter loaded"
