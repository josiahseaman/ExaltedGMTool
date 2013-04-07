from django.contrib.localflavor import us
from ElementTree import *


class ExaltedCharacter():

    def __init__(self, filename=None):
        self.accuracy = 1
        self.damageCode = 1
        self.DV = 1
        self.soak = 1
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
    
if __name__ == "__main__":
    c = ExaltedCharacter('Willow.ecg')
    usefulStats = ['Charisma', 'Presence', 'Perception', 'Awareness', 'Dodge', 'Survival', 'Computers']

    for stat in usefulStats:
        print stat, ":", int(c.getStat(stat) or 0)
