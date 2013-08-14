from ExaltedCharacter import ExaltedCharacter
import copy
from TemporaryStat import HealthLevel

'''Features:==

==Still Needed:==

'''


class BattleWheel():
    def rollInitiative(self, newCharacters):
        if not newCharacters:
            return
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
                    print "Removing", current
                    self.removeCharacter(current)
                    current = None
            except:
                self.currentTick += 1
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

    def moveCurrentCharacterForward(self, speed=5):
        ch = self.getCurrentCharacter()
        self.addCharacterToTick(ch, self.currentTick + speed)
        self.tickLayout[self.currentTick].remove(ch)  #remove from the old position
        print "Done with", ch


class CombatScene():
    def __init__(self, PlayerCharacters):
        self.characters = {}
        self.current = None
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
            newChar.name += str(n+1)  # adds a number to the mook

            self.addCharacter(newChar)

    def beginBattle(self):
        self.battleWheel = BattleWheel(self.characters.values())
        self.current = self.battleWheel.getCurrentCharacter()
        print self.battleWheel.tickLayout
        return self.battleWheel.getCurrentCharacter()

    def resolve(self, speed=5):
        self.battleWheel.moveCurrentCharacterForward(speed)
        self.current = self.battleWheel.getCurrentCharacter()
        self.current.refreshDV()
        print "It is", str(self.current) + "'s turn to act."
        return self.current

#c = sc.beginBattle()
#c = sc.resolve()