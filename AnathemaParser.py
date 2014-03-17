__author__ = 'Josiah'
from xml.etree.ElementTree import ElementTree
from Glossary import *


class AnathemaParser:
    def __init__(self, filename):
        tree = ElementTree(file=filename)
        self.root = tree.getroot()
        self.sheet = {}

    def parse_text_fields(self):
        text_fields = [('Name', 'CharacterName'), 'Player', 'Concept', ('Type', 'CharacterType'), ]
        for t in text_fields:
            if isinstance(t, tuple):
                self.populate_text_field(*t)
            else:
                self.populate_text_field(t)

    def parse_to_dictionary(self):
        self.parse_text_fields()

        self.sheet['Specialties'] = {}
        numeric_fields = [essence, willpower, compassion, conviction, temperance, valor, strength, dexterity, dex,
                          stamina, charisma, manipulation, appearance, perception, intelligence, wits, craft, archery,
                          martialarts, melee, thrown, war, integrity, performance, presence, resistance, survival,
                          investigation, lore, medicine, occult, athletics, awareness, dodge, larceny, stealth,
                          bureaucracy, linguistics, ride, sail, socialize, limit,]
        for x in numeric_fields:
            self.populate_numeric_field(x)


        lists = ['Spells', 'Combos', 'Charms', 'Backgrounds']
        return self.sheet

    def populate_text_field(self, field_name, anathema_name = ''):
        if not anathema_name:
            anathema_name = field_name
        element = next(self.root.iter(anathema_name))
        self.sheet[field_name] = self.getText(element)

    def populate_numeric_field(self, field_name):
        self.sheet[field_name] = self.getStat(field_name)
        self.sheet['Specialties'][field_name] = self.getSpecialty()

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

    def getText(self, elem):
        return ",".join(elem.itertext())
