
from ExaltedCharacter import ExaltedCharacter

class CombatScene():
    def __init__(self):
        self.characters = {}
        # self.ticker = BattleWheel()
    def addCharacter(self, character):
        self.characters[character.name] = character

def testScene(nAttacks=3):
    caedris = ExaltedCharacter('Caedris.ecg')
    willow = ExaltedCharacter('Willow.ecg')
    caedris.flurryAttack(nAttacks, willow)

if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="
    testScene()

