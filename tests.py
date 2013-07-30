__author__ = 'seaman'

import unittest


import Scene
class SceneTest(unittest.TestCase):

    def testAccuracy(self):
        import ExaltedCharacter as e
        c = e.ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')
        self.assertEqual(c.accuracy(), 9)

    def testDamage(self):
        import ExaltedCharacter as e
        c = e.ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')
        self.assertEqual(c.damageCode(), 7)
        print c.sumDicePool('Essence')

    def testMembership(self):
        scene = Scene.CombatScene(False)
        self.assertEqual(len(scene.characters), 0)
        import ExaltedCharacter
        c = ExaltedCharacter.ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
        scene.addCharacter(c)
        scene.beginBattle()
        self.assertEqual(len(scene.battleWheel.activeCharacters), 1)
        scene.battleWheel.removeCharacter(c)
        self.assertEqual(len(scene.battleWheel.activeCharacters), 0)
        self.assertFalse(any([c in tick for tick in scene.battleWheel.tickLayout.values()]))

    def testBeginScenario(nAttacks=3):
        scene = Scene.CombatScene()
        scene.beginScenario()
        print 'Done'


class CharacterTest(unittest.TestCase):
    import ExaltedCharacter
    c = ExaltedCharacter.ExaltedCharacter('Willow.ecg')

    def testPrintAttributes(self):
        print self.c.name
        usefulStats = ['Charisma', 'Presence', 'Survival', 'Computers']

        for stat in usefulStats:
            print stat, ":", int(self.c.getStat(stat) or 0)
        print "For 'Perception', 'Awareness' Roll", self.c.sumDicePool('Perception', 'Awareness'), "dice"

    def testDerivedStats(self):
        print "Stat test"
        self.assertEqual(self.c['Essence'], 4)
        self.assertEqual(self.c.peripheralEssence, 43)
        self.assertEqual(self.c.personalEssence, 18)

    def testRunningOut(self):
        self.c.roll('Compassion', 'Dexterity')
        self.c.roll('Compassion', 'Dexterity')
        self.assertRaises(ValueError, self.c.roll, 'Compassion', 'Dexterity' )

    def chooseWeaponTest(self):
        import ExaltedCharacter
        gin = ExaltedCharacter.ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')


if __name__ == '__main__':
    unittest.main()
