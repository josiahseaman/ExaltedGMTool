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

    def testChooseWeapon(self):
        import ExaltedCharacter
        gin = ExaltedCharacter.ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
        self.assertEqual(gin.armorStats['name'], 'Superheavy Plate (Artifact)')
        self.assertEqual(gin.weaponStats['name'], 'Grand Goremaul')

    def testChooseAttackSkill(self):
        import ExaltedCharacter
        blix = ExaltedCharacter.ExaltedCharacter('Blixorthodon.ecg')
        self.assertEqual(blix.accuracy(), 13)
        blix.weaponStats = blix.parseWeapon('equipment/War_Boomerang.item')
        self.assertEqual(blix.accuracy(), 4) #this should be using Thrown, because of the thrown tag stat block under knife

    def testCraftSkillRoll(self):
        import ExaltedCharacter
        swift = ExaltedCharacter.ExaltedCharacter('WarrickSwiftColson.ecg')
        self.assertEqual(swift.getStat('Craft'),4)



if __name__ == '__main__':
    unittest.main()
