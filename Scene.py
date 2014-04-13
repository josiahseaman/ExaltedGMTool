from ExaltedCharacter import ExaltedCharacter
import copy
from TemporaryStat import HealthLevel

'''Features:==

==Still Needed:==

'''


class BattleWheel():
    def __init__(self, allCharacters):
        self.tickLayout = {}
        self.currentTick = 0
        self.reactionCount = 0
        self.activeCharacters = allCharacters  # all characters are assumed to be active at first, but can become
                                               # inactive if they are injured or knocked out
        self.rollInitiative(allCharacters)

    def __repr__(self):
        return "BattleWheel:" + self.tickLayout.__repr__()

    def rollInitiative(self, newCharacters):
        if not newCharacters:
            return
        initiatives = {}
        for character in newCharacters:
            initiatives[character] = character.joinBattle()
        self.reactionCount = max(self.reactionCount, max(initiatives.values()))
        for character, initiative in list(initiatives.items()):
            self.addCharacterToTick(character, self.reactionCount - initiative + self.currentTick)

    def addCharacterToTick(self, character, tick):
        if isinstance(tick, ExaltedCharacter): # swap confused arguments, my bad
            tmp = tick
            tick = character
            character = tmp
        lineup = self.tickLayout.get(tick,[])
        lineup.append(character)
        self.tickLayout[tick] = lineup

    def getCurrentCharacter(self):
        current = None
        while not current:
            current = self.tickLayout.get(self.currentTick,[])[:1]
            try:
                current = current[0]
                if current.isDying:
                    print("Removing", current)
                    self.removeCharacter(current)
                    current = None
            except:
                self.currentTick += 1
        return current

    def removeCharacter(self, character):
        try:
            self.activeCharacters.remove(character)
            for tick in list(self.tickLayout.values()):
                if character in tick:
                    tick.remove(character)
            return True
        except:
            print("I didn't find the character", character)
            return False

    def moveCurrentCharacterForward(self, speed=5):
        ch = self.getCurrentCharacter()
        self.addCharacterToTick(ch, self.currentTick + speed)
        self.tickLayout[self.currentTick].remove(ch)  #remove from the old position
        print("Done with", ch)


class CombatScene():
    def __init__(self, activeCharacters):
        self.characters = {}
        self.current = None
        self.battleWheel = None
        self.globalMookCount = 0
        for character in activeCharacters:
            self.addCharacter(character)

    def __getitem__(self, item):
        return self.characters.get(item, None)

    def addCharacter(self, character):
        self.characters[character.name] = character
        if self.battleWheel is not None:
            self.battleWheel.rollInitiative([character])

    def addExtras(self, nDuplicates, character):
        self.addDuplicates(nDuplicates, character, True)

    def addDuplicates(self, nDuplicates, character, isExtra=False):
        assert isinstance(character, ExaltedCharacter)
        for n in range(nDuplicates):
            newChar = copy.deepcopy(character)
            if isExtra:
                newChar.health = HealthLevel('Health Levels', 3)  # Extras only have three health levels, instead of 7
            self.globalMookCount += 1
            newChar.name += str(self.globalMookCount)  # adds a number to the mook name
            self.addCharacter(newChar)

    def beginBattle(self):
        self.battleWheel = BattleWheel(list(self.characters.values()))
        self.current = self.battleWheel.getCurrentCharacter()
        print()
        print(self.battleWheel.tickLayout)
        return self.current

    def groupAttack(self, mookTypeName, targetCharacter):
        while mookTypeName in self.current.name and not targetCharacter.isDying:
            self.current.attack(targetCharacter)
            self.resolve()
        print(targetCharacter, targetCharacter.health)

    def resolve(self, actionName=None):
        """resolve() now takes actionName or None since character state can handle speed and DV penalty internally."""
        if actionName:
            self.current.handleAction(actionName)
        self.resolveManual(self.current.longestActionSpeed)

    def resolveManual(self, speed=5):
        self.battleWheel.moveCurrentCharacterForward(speed)
        self.current = self.battleWheel.getCurrentCharacter()
        self.current.refreshDV()
        print("It is", str(self.current) + "'s turn to act.")
        return self.current
