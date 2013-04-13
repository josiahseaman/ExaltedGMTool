
from ExaltedCharacter import ExaltedCharacter

class BattleWheel():
    def __init__(self):
        self.tickLayout = {}
        self.currentTick = 0
        self.reactionCount = 0

    def beginBattle(self, allCharacters):
        initiatives = {}
        for character in allCharacters:
            initiatives[character] = character.joinBattle()
        self.reactionCount = max(initiatives.values())
        for character, initiative in initiatives.items():
            self.addCharacterToTick(character, self.reactionCount - initiative + self.currentTick)

    def addCharacterToTick(self, character, tick):
        lineup = self.tickLayout.get(tick,[])
        lineup.append(character)
        self.tickLayout[tick] = lineup

    def fetchCurrentCharacter(self):
        current = None
        while not current:
            current = self.tickLayout.get(self.currentTick,[])[:1]
            try: current = current[0]
            except: self.currentTick += 1
        return current

    def nextAction(self):
        current = self.fetchCurrentCharacter()
        print "It is ", current, " turn to act."
        return current

    def resolveAction(self, speed=5):
        ch = self.fetchCurrentCharacter()
        self.addCharacterToTick(ch, self.currentTick + speed)
        self.tickLayout[self.currentTick].remove(ch) #remove from the old position
        print "Done with", ch

    def testBattleWheel(self):
        caedris = ExaltedCharacter('Caedris.ecg')
        self.addCharacterToTick(caedris, 4)
        print self.tickLayout

class CombatScene():
    def __init__(self):
        self.characters = {}
        self.battleWheel = BattleWheel()

    def addCharacter(self, character):
        self.characters[character.name] = character

    def beginBattle(self):
        self.battleWheel.beginBattle(self.characters.values())
        print self.battleWheel.tickLayout

    def beginScenario(self):
        self.beginBattle()
        for i in range(5):
            actor = self.battleWheel.nextAction()
            actor.flurryAttack(3, actor)#do stuff
            self.battleWheel.resolveAction(speed=5)


def testScene(nAttacks=3):
    scene = CombatScene()
    caedris = ExaltedCharacter('Caedris.ecg')
    willow = ExaltedCharacter('Willow.ecg')
    scene.addCharacter(caedris)
    scene.addCharacter(willow)
    scene.beginScenario()

    # caedris.flurryAttack(nAttacks, willow)

if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="
    testScene()

