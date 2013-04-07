from django.contrib.localflavor import us
from ElementTree import *


class ExaltedCharacter():

    def __init__(self, filename=None):
        self.accuracy = 11
        self.damageCode = 4
        self.DV = 3
        self.soak = 4
        self.characterSheet = None
        if filename:
            self.characterSheet = self.parseXML(filename)

    def parseXML(self, filename):
        """:return: Root node of the XML character sheet"""
        tree = ElementTree(file=filename)
        root = tree.getroot()
        return root

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


if __name__ == "__main__":
    c = ExaltedCharacter('Willow.ecg')
    usefulStats = ['Charisma', 'Presence', 'Perception', 'Awareness', 'Dodge', 'Survival', 'Computers']

    for stat in usefulStats:
        print stat, ":", int(c.getStat(stat) or 0)
    print "For 'Perception', 'Awareness' Roll", c.sumDicePool('Perception', 'Awareness'), "dice"
