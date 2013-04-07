
from ExaltedCharacter import ExaltedCharacter


def testScene(nAttacks=3):
    dace = ExaltedCharacter()
    swift = ExaltedCharacter()
    dace.flurryAttack(nAttacks, swift)

if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="
    testScene()

