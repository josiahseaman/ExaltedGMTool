from django.contrib.localflavor import us
from ElementTree import *
from DiceRoller import *
import json


class ExaltedCharacter():

    def __init__(self, filename=None):
        self.name = "Unnamed"
        self.characterSheet = None
        if filename:
            self.characterSheet = self.parseXML(filename)
            self.name = self.getName()
        self.weaponStats = json.load(open('Daiklave.item'))
        self.armorStats = json.load(open('Articulated_Plate.item'))

    def __repr__(self):
        return self.name

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

    def soak(self):
        return self.sumDicePool('Stamina')/2 + self.armorStats["statsByRuleSet"]["SecondEdition"][0]["soakByHealthType"]['Lethal']

    def hardness(self):
        return self.armorStats["statsByRuleSet"]["SecondEdition"][0]["hardnessByHealthType"]['Lethal']

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

    def getText(self, elem):
        print elem
        return ",".join(elem.itertext())

    def sumDicePool(self, *stats):
        dicePool = 0
        for stat in stats: #I can do this with reduce, but it's harder to read
            dicePool += self.getStat(stat)
        return dicePool

    def roll(self, *stats):
        return skillCheckByNumber(self.sumDicePool(*stats))

    def flurryAttack(self, nAttacks,  defendingChar):
        return flurry(nAttacks, self.accuracy(), self.damageCode(), defendingChar.DV(), defendingChar.soak(), defendingChar.hardness())

    def joinBattle(self):
        return self.roll('Wits', 'Awareness')

if __name__ == "__main__":
    c = ExaltedCharacter('Willow.ecg')
    print c.name
    usefulStats = ['Charisma', 'Presence', 'Perception', 'Awareness', 'Dodge', 'Survival', 'Computers']

    for stat in usefulStats:
        print stat, ":", int(c.getStat(stat) or 0)
    print "For 'Perception', 'Awareness' Roll", c.sumDicePool('Perception', 'Awareness'), "dice"
