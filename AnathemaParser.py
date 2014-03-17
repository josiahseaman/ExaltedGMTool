__author__ = 'Josiah'
from xml.etree.ElementTree import ElementTree



class AnathemaParser:
    def __init__(self, filename):
        tree = ElementTree(file=filename)
        self.root = tree.getroot()

    def parse_to_dictionary(self):
        sheet = {}
        sheet['Name'] = self.root.attrib['repositoryPrintName']
        return sheet

    def getStatNumber(self, element):
        result = element.get('experiencedValue', None)
        if not result:
            result = element.get('creationValue', None)
        return int(result or 0)

    def getStat(self, statName):
        statName = statName.lower().capitalize()  #proper capitalization
        # try: return self.magicalEffects[statName]
        # except: pass
        if statName == 'Martialarts':
            statName = 'MartialArts'
        try:
            element = next(self.characterSheet.iter(statName))
        except:
            raise KeyError(str(statName) + ": No such stat")
        if statName == 'Craft':
            branches = element.getiterator('subTrait')
            result = max(list(map(self.getStatNumber, branches)))
        else:
            result = self.getStatNumber(element)

        #check for specialties, assumes they are applicable to this roll
        try:
            specialtyElem = next(element.iter('Specialty'))
            print("Specialty:", specialtyElem.attrib['name'], end=' ')
            #currently I'm print this out to remind people of the assumption
            specialty = self.getStatNumber(specialtyElem)
        except:
            specialty = 0
        result += specialty
        return result

    def gearList(self):
        models = self.additionalModels()
        gearNames = []
        for i in range(1, 20):  # try grabbing a gear name
            try:
                gearNames.append(next(models['Equipment'][0][i][0].itertext()))
            except:
                pass
        return gearNames

    def additionalModels(self):
        e = next(self.characterSheet.getiterator('AdditionalModels'))
        availableModels = {x.get('templateId'): x for x in e.getchildren()}
        return availableModels
