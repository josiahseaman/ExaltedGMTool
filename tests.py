__author__ = 'seaman'

import unittest


class MyTestCase(unittest.TestCase):

    def testAccuracy(self):
        import ExaltedCharacter as e
        c = e.ExaltedCharacter('Caedris.ecg')
        self.assertEqual(c.accuracy(), 10)

    def testDamage(self):
        import ExaltedCharacter as e
        c = e.ExaltedCharacter('Caedris.ecg')
        self.assertEqual(c.damageCode(), 7)
        print c.sumDicePool('Essence')


    def testScene(nAttacks=3):
        import Scene
        import ExaltedCharacter
        scene = Scene.CombatScene()
        caedris = ExaltedCharacter.ExaltedCharacter('Caedris.ecg')
        willow = ExaltedCharacter.ExaltedCharacter('Willow.ecg')
        scene.addCharacter(caedris)
        scene.addCharacter(willow)
        # scene.beginScenario()
        print 'Done'


class CharacterTest(unittest.TestCase):
    import ExaltedCharacter
    c = ExaltedCharacter.ExaltedCharacter('Willow.ecg')

    def testprintAttributes(self):
        print self.c.name
        usefulStats = ['Charisma', 'Presence', 'Survival', 'Computers']

        for stat in usefulStats:
            print stat, ":", int(self.c.getStat(stat) or 0)
        print "For 'Perception', 'Awareness' Roll", self.c.sumDicePool('Perception', 'Awareness'), "dice"

    def testderivedStats(self):
        print "Stat test"
        self.assertEqual(self.c['Essence'], 4)
        self.assertEqual(self.c.peripheralEssence, 42)
        self.assertEqual(self.c.personalEssence, 17)

if __name__ == '__main__':
    unittest.main()
