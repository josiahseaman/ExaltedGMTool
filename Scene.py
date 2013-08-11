from ExaltedCharacter import ExaltedCharacter
from ExaltedCharacter import HealthLevel
import copy

'''Features:==

==Still Needed:==

'''


class BattleWheel():
    def rollInitiative(self, newCharacters):
        initiatives = {}
        for character in newCharacters:
            initiatives[character] = character.joinBattle()
        self.reactionCount = max(self.reactionCount, max(initiatives.values()))
        for character, initiative in initiatives.items():
            self.addCharacterToTick(character, self.reactionCount - initiative + self.currentTick)

    def __init__(self, allCharacters):
        self.tickLayout = {}
        self.currentTick = 0
        self.reactionCount = 0
        self.activeCharacters = allCharacters  # all characters are assumed to be active at first, but can become
                                               # inactive if they are injured or knocked out
        self.rollInitiative(allCharacters)

    def addCharacterToTick(self, character, tick):
        lineup = self.tickLayout.get(tick,[])
        lineup.append(character)
        self.tickLayout[tick] = lineup

    def fetchCurrentCharacter(self):
        current = None
        while not current:
            current = self.tickLayout.get(self.currentTick,[])[:1]
            try:
                current = current[0]
                if current.isDying:
                    print "Removing", current
                    self.removeCharacter(current)
                    current = None
            except:
                self.currentTick += 1
        current.refreshDV()
        return current

    def removeCharacter(self, character):
        try:
            self.activeCharacters.remove(character)
            for tick in self.tickLayout.values():
                if character in tick:
                    tick.remove(character)
            return True
        except:
            print "I didn't find the character"
            return False

    def nextAction(self):
        if len(self.activeCharacters) <= 1:
            raise StopIteration
        current = self.fetchCurrentCharacter()
        print "It is", current, " turn to act."
        return current

    def resolveAction(self, speed=5):
        ch = self.fetchCurrentCharacter()
        self.addCharacterToTick(ch, self.currentTick + speed)
        self.tickLayout[self.currentTick].remove(ch) #remove from the old position
        print "Done with", ch


class CombatScene():
    def __init__(self, PlayerCharacters):
        self.characters = {}
        self.battleWheel = None
        for character in PlayerCharacters:
            self.addCharacter(character)

    def addCharacter(self, character):
        self.characters[character.name] = character
        if self.battleWheel is not None:
            self.battleWheel.rollInitiative([character])

    def addExtras(self, nDuplicates, character):
        assert isinstance(character, ExaltedCharacter)
        character.health = HealthLevel('Health Levels', 3)
        for n in range(nDuplicates):
            newChar = copy.deepcopy(character)
            newChar.name += str(n+1) # adds a number to the mook

            self.addCharacter(newChar)

    def beginBattle(self):
        self.battleWheel = BattleWheel(self.characters.values())
        print self.battleWheel.tickLayout
        return self.next()

    def next(self):
        return self.battleWheel.nextAction()

    def resolve(self, speed=5, DvPenalty=1):
        self.battleWheel.resolveAction(speed)
        return self.next()

#c = sc.beginBattle()
#c = sc.resolve()