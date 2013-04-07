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

    def parseXML(self):
        """
        :return: Root node of the XML character sheet
        """
        filename = 'Willow.ecg'
        tree = ElementTree(file=filename)
        # the tree root is the toplevel html element
        print tree.findtext("ExaltedCharacter")

        # if you need the root element, use getroot
        root = tree.getroot()
        return root

    def getStat(self, statName):
        try:
            element = root.getiterator(statName).next()
        except:
            return None
        result = element.get('experiencedValue',None)
        if not result:
            result = element.get('creationValue', None)
        return result

    def getText(self, elem):
        print elem
        return ",".join(elem.itertext())
    
if __name__ == "__main__":
    c = ExaltedCharacter()
    root = c.parseXML()
    # print tostring(root)
    usefulStats = ['Charisma', 'Presence', 'Perception', 'Awareness', 'Dodge', 'Resistance', 'Computers']
    for stat in usefulStats:
        print stat, ":", c.getStat(stat)
    # print root.find('Statistics')
