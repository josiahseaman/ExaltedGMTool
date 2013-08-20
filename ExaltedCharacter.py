import json
import re

from ElementTree import *
from DiceRoller import *
from TemporaryStat import TemporaryStat, HealthLevel, RulesError
from collections import namedtuple


def halfRoundUp(raw):
    return int(raw / 2.0 + .5)


Action = namedtuple('Action', ['name', 'speed', 'dv'])
spec = [("Attack", None, -1),  # None means that it varies, as opposed to -0 DV penalty
        # ("Flurry", None, None),
        ("Clinch", 6, -10),  # I think you lose your DV against others when you clinch someone
        ("Guard", 3, 0),  # Holding Action
        ("Aim", 3, -1),  # Holding Action
        ("Ready Weapon", 5, 0),
        ("Performance", 6, -2),
        ("Presence", 5, -2),
        ("Investigation", 5, -2),
        ("Coordinate Attack", 5, 0),
        ("Simple Charm", 6, -1),
        ("Defend Other", 5, 0),
        ("Dash", 3, -2),
        ("Jump", 5, -1),
        ("Rise from Prone", 5, -1),
        ("Miscellaneous", 5, -1),
        ("Inactive", 5, -20)
]
actions = {x[0]: Action(*x) for x in spec}  # dict declaration by comprehension, storing Actions by their name

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
        self.limit = self.newStat('Limit', 10, 0)
        self.CompassionChannel = self.newStat('Compassion')
        self.ConvictionChannel = self.newStat('Conviction')
        self.TemperanceChannel = self.newStat('Temperance')
        self.ValorChannel = self.newStat('Valor')
        self.magicalEffects = {}

        self.dvPenalty = 0
        self.longestActionSpeed = 3
        self.clinchedCharacter = None
        self.actionsRemaining = TemporaryStat("Actions Remaining", 1)

    def __repr__(self):
        return "<" + self.name + ">"

    def newStat(self, name, maximum=None, temporary=None):
        """This is just a convenience function for grabbing the value from the character sheet"""
        if maximum is None:
            return TemporaryStat(name, self[name], temporary)
        else:
            return TemporaryStat(name, maximum, temporary)

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
        stats = raw["statsByRuleSet"]["SecondEdition"][0] #grabs the entire stat block

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
        return halfRoundUp(self.sumDicePool('Dexterity', 'Dodge', 'Essence') + self.armorStats.get('mobilityPenalty',0))

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
        # try: return self.magicalEffects[statName]
        # except: pass
        if statName == 'Martialarts': statName = 'MartialArts'
        try:
            element = self.characterSheet.iter(statName).next()
        except:
            raise KeyError(str(statName) + ": No such stat")
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

    def internalPenalties(self):
        return self.health.woundPenalty()  #TODO:  + self.flurryPenalty() + self.magicalEffects['internalPenalty']

    def sumDicePool(self, *stats):
        dicePool = 0
        for stat in stats: #I can do this with reduce, but it's harder to read
            try:
                dicePool += self[stat]
            except AttributeError:
                dicePool += stat #this is probably a number
        return max(0, dicePool + self.internalPenalties())

    def rollWithPenalties(self, dicePool, label=None):
        """Please use self.rollWithPenalties when you need to calculate dicepools by hand.
        Example: roll highest of Manipulation/Charisma with Presence, Performance, or Investigation."""
        dicePool = max(0, dicePool + self.internalPenalties())
        return skillCheckByNumber(dicePool, label)  # TODO: + self.magicalEffects['externalPenalty']

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

    def flurry(self, nActions):
        """ This simply declares that the player intends to take multiple actions in a single tick.
            It is necessary to know how many actions they're taking beforehand in order to calculate dice penalties."""
        self.actionsRemaining = TemporaryStat("Actions Remaining", nActions)

    def attack(self, defendingChar):
        damageDealt = attackRoll(self.accuracy(), self.damageCode(), defendingChar.DV(), defendingChar.soak(),
                                 defendingChar.hardness(), self.weaponStats.get('minimumDamage', 1))
        self.addDvPenalty(1)
        defendingChar.takeDamage(damageDealt)
        return damageDealt

    def flurryAttack(self, nAttacks, defendingChar, hasPenalty=True):
        """This is a convenience function for the user to be able to declar a flurry containing nothing but attacks."""
        # Make sure the action declaration is following the existing flurry rules
        if self.actionsRemaining.temporary < nAttacks and self.actionsRemaining.permanent > 1:
            raise RulesError("You have already declared a flurry and you don't have enough action remaining.")
        elif self.actionsRemaining.permanent == 1:  # If you haven't called flurry yet, I'll do it for you
            self.flurry(nAttacks)

        penalties = range(nAttacks-1, (nAttacks-1)+nAttacks) if hasPenalty else [0]*nAttacks
        for onslaught, penalty in enumerate(penalties):
            if defendingChar.isDying:
                print "Select a new target! You have", self.actionsRemaining
                return False
            damageDone = attackRoll(self.accuracy()-penalty, self.damageCode(), max(0, defendingChar.DV()-onslaught),
                                    defendingChar.soak(), defendingChar.hardness(), self.weaponStats.get('minimumDamage', 1))
            self.handleAction('Attack', hasPenalty)
            defendingChar.takeDamage(damageDone)
        return True

    def clinch(self, defendingChar):
        dice = self.clinchPool()
        threshold = toHit(dice, defendingChar.DV())
        if threshold > -1:
            self.clinchedCharacter = defendingChar
            defendingChar.handleAction('Inactive')
        #TODO: Add options: Throw, Crush, Hold
        # if "Throw":
        #     #damage
        #     self.clinchedCharacter = None
        # if "Crush":
        #     damage = threshold + self['Strength']
        self.handleAction('Clinch')
        return threshold

    def clinchPool(self):
        return max(self.sumDicePool('Strength', 'MartialArts'), self.sumDicePool('Dexterity', 'MartialArts'))

    def maintainClinch(self):
        if self.clinchedCharacter is not None:
            aggressor = skillCheckByNumber("Maintain Grapple", self.clinchPool())
            self.clinchedCharacter.dvPenalty = 0
            defense = skillCheckByNumber("Break Grapple", self.clinchedCharacter.clinchPool())
            if aggressor >= defense:
                print "You maintain the clinch"
                self.handleAction('Clinch')
                return True
            else:
                print "Your victim has become your master!  Prepare to die."
                self.clinchedCharacter.clinchedCharacter = self  # they are now clinching you
                self.clinchedCharacter = None  # and you aren't clinching them
                self.handleAction('Inactive')
                return False

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
            self.actionsRemaining = TemporaryStat("Actions Remaining", 1)  # this can be raised by declaring a flurry
            self.dvPenalty = 0 # remove dv penalties
            self.longestActionSpeed = 3
            self.maintainClinch()# maintain clinch
            # if self['Player'] != 'NPC':
            self.regain(5)  # TODO: only regen for Player Characters

    def handleAction(self, actionName, hasPenalty=True):
        """handleAction() now takes the name of an action and applies dvPenalty and speed (can be weapon) to the
        character.  hasPenalty=False acts like an extra action charm."""
        action = actions[actionName]
        self.actionsRemaining -= 1  # TemporaryStat
        if hasPenalty:
            self.dvPenalty += action.dv
        else:  # for extra action charms that only apply the highest DV penalty
            self.dvPenalty = min(self.dvPenalty, action.dv)  # min because the "largest" penalty is negative
        speed = action.speed if action.speed is not None else self.weaponStats["speed"]
        self.longestActionSpeed = max(self.longestActionSpeed, speed)


    '''SOCIAL COMBAT'''
    def parryMDV(self):
        raw = max(self["Charisma"], self["Manipulation"]) + \
              max(self["Investigation"], self["Performance"], self["Presence"], self["Socialize"]) + \
              self.health.woundPenalty()  # Wound penalty here because we are not using sumDicePool
        return halfRoundUp(raw) # Round Up

    def dodgeMDV(self):  # Round down
        return (self.sumDicePool('Willpower', 'Integrity', 'Essence') ) / 2

    def MDV(self):
        return max(self.dodgeMDV(), self.parryMDV())

    def appearanceAdjustment(self, attackingChar):
        #Adjust for Appearance
        appearanceAdjustment = self['Appearance'] - attackingChar['Appearance']
        #TODO: Account for Appearance 0 being a bonus sometimes...
        appearanceAdjustment = max(-3, min(appearanceAdjustment, 3))
        return appearanceAdjustment

    def adjustedMDV(self, attackingChar, isMotivationFavorable, isVirtueFavorable, isIntimacyFavorable):
        """Adjust DV for Appearance, motivation, virtue, and intimacy"""
        mapping = {True: -1, False: 1, None: 0} # Giving numerical values for our True/False answers
        factors = [isIntimacyFavorable, isVirtueFavorable,
                   isMotivationFavorable]  # arranged in order of increasing importance
        factors = map(lambda x: mapping[x], factors)
        factors = [x * (i + 1) for i, x in enumerate(factors)]  # factors are arranged in increasing importance = 1,2,3
        negatives = min(
            filter(lambda x: x < 0, factors) + [0])  # we are adding a zero to our list to avoid the empty list error
        positives = max(
            filter(lambda x: x > 0, factors) + [0])  # we are adding a zero to our list to avoid the empty list error
        effectiveMDV = max(0, self.MDV() + negatives + positives + self.appearanceAdjustment(attackingChar))
        return effectiveMDV

    def socialAttack(self, defendingChar, ability=None, isMotivationFavorable=None, isVirtueFavorable=None, isIntimacyFavorable=None):
        if ability is None:
            ability = max(self["Investigation"], self["Performance"], self["Presence"])
        else:
            ability = self[ability]  # turn this name string into a number off your character sheet
        #Pick either charisma or manipulation
        attribute = max(self["Charisma"], self["Manipulation"])  # TODO: allow selecting Charisma/Manipulation

        theirEffectiveMDV = defendingChar.adjustedMDV(self, isMotivationFavorable, isVirtueFavorable, isIntimacyFavorable)
        successes = self.rollWithPenalties(attribute + ability, "Social Attack")
        threshold = successes - theirEffectiveMDV
        if successes >= theirEffectiveMDV:
            print "Beat MDV of", theirEffectiveMDV, "with", threshold, "threshold successes"
            if threshold >= 3:  # per errata: "Threshold Successes on Social Attacks"
                print "+" + str(threshold/3), "Willpower to resist"
        else:
            print "You are not convincing! ", successes, "successes vs. their", theirEffectiveMDV, "MDV."
        return 1 + threshold / 3  # Willpower cost to resist this (no charms)


if __name__ == "__main__":
    print "ExaltedCharacter loaded"
