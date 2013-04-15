from django.contrib.localflavor import us
from ElementTree import *
from DiceRoller import *
import json


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
        self.temporary = min( self.temporary + amount, self.permanent)
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
            self.characterSheet = self.parseXML(filename)
            self.name = self.getName()
        self.virtues = ['Compassion', 'Conviction', 'Temperance', 'Valor']
        self.weaponStats = json.load(open('Daiklave.item'))
        self.armorStats = self.parseArmor('Articulated_Plate__Artifact_.item')
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
        return self['Essence'] * 7 + self['Willpower'] + sum(self[x] for x in self.virtues) # - committed artifacts - permanent charms



    '''Items Stats'''
    def parseArmor(self, filename):
        stats = {}
        raw = json.load(open('equipment/' + filename))
        statBlock = raw["statsByRuleSet"]["SecondEdition"]
        stats['lethalSoak'] = statBlock[0]["soakByHealthType"]['Lethal']
        stats['bashingSoak'] = statBlock[0]["soakByHealthType"]['Bashing']
        stats['lethalHardness'] = statBlock[0]["hardnessByHealthType"]['Lethal']
        stats['bashingHardness'] = statBlock[0]["hardnessByHealthType"]['Bashing']
        stats["fatigue"] = statBlock[0]["fatigue"]
        stats["mobilityPenalty"] = statBlock[0]["mobilityPenalty"]
        stats["attuneCost"] = statBlock[1]["attuneCost"]
        return stats

    def accuracy(self):
        return self.weaponStats["statsByRuleSet"]['SecondEdition'][0]['accuracy'] + self.sumDicePool('Dexterity', "Melee")

    def damageCode(self):
        return self.weaponStats["statsByRuleSet"]['SecondEdition'][0]['damage'] + self.sumDicePool('Strength',)

    def parryDV(self):
        return (self.weaponStats["statsByRuleSet"]['SecondEdition'][0]['defence'] + self.sumDicePool('Dexterity', "Melee"))/2

    def dodgeDV(self):
        return (self.sumDicePool('Dexterity', 'Dodge', 'Essence'))/2

    def DV(self):
        return max(self.parryDV(), self.dodgeDV())

    def soak(self, damageType='lethal'):
        soakType = damageType + 'Soak'
        return self.sumDicePool('Stamina')/2 + self.armorStats[soakType]

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
            print "Specialty:", specialtyElem.attrib['name'], #currently I'm print this out to remind people of the assumption
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
        return dicePool

    def channelVirtue(self, virtue):
        attribName = virtue + 'Channel'
        self.__dict__[attribName] -= 1
        return self[virtue]

    def roll(self, *stats):
        autoSuccesses = 0
        bonusDice = 0
        if (stats[0].lower() == 'willpower' or stats[0] in self.virtues) and len(stats) > 1:
            self.temporaryWillpower -= 1 #even if this is a virtue channel it still takes 1wp
            if stats[0].lower() == 'willpower':
                autoSuccesses += 1
            else: #This is a virtue
                bonusDice += self.channelVirtue(stats[0])#mark off virtue channel
            stats = stats[1:]#remove from list

        rolledDice = skillCheckByNumber(self.sumDicePool(*stats) + bonusDice)
        return rolledDice + autoSuccesses

    def flurryAttack(self, nAttacks,  defendingChar):
        return flurry(nAttacks, self.accuracy(), self.damageCode(), defendingChar.DV(), defendingChar.soak(), defendingChar.hardness())

    def joinBattle(self):
        return self.roll('Wits', 'Awareness')

if __name__ == "__main__":
    c = ExaltedCharacter('Willow.ecg')
    print c.name
    usefulStats = ['Charisma', 'Presence', 'Survival', 'Computers']

    for stat in usefulStats:
        print stat, ":", int(c.getStat(stat) or 0)
    print "For 'Perception', 'Awareness' Roll", c.sumDicePool('Perception', 'Awareness'), "dice"
