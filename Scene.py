from ExaltedCharacter import ExaltedCharacter

PlayerCharacters = ['Blixorthodon', 'Caedris', 'Gin', 'Skogur', 'WarrickSwiftColson', 'Willow', 'ZaelaPrismaticUnfoldingLotus']

class BattleWheel():
    def __init__(self, allCharacters):
        self.tickLayout = {}
        self.currentTick = 0
        self.reactionCount = 0
        self.activeCharacters = allCharacters  # all characters are assumed to be active at first, but can become
                                               # inactive if they are injured or knocked out
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

    def testBattleWheel(self):
        caedris = ExaltedCharacter('Caedris.ecg')
        self.addCharacterToTick(caedris, 4)
        print self.tickLayout


class CombatScene():
    def __init__(self, includePCs=True):
        self.characters = {}
        self.battleWheel = None
        if includePCs:
            for character in PlayerCharacters:
                ExChar = ExaltedCharacter(character)
                self.addCharacter(ExChar)

    def addCharacter(self, character):
        self.characters[character.name] = character

    def beginBattle(self):
        self.battleWheel = BattleWheel(self.characters.values())
        print self.battleWheel.tickLayout

    def beginScenario(self):
        self.beginBattle()
        for i in range(5):
            actor = self.battleWheel.nextAction()
            actor.flurryAttack(1, actor)#do stuff
            self.battleWheel.resolveAction(speed=5)


if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="

