__author__ = 'seaman'

import unittest


import Scene
class SceneTest(unittest.TestCase):
    import ExaltedCharacter as e
    caedris = e.ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')

    def testAccuracy(self):
        self.assertEqual(self.caedris.accuracy(), 9)

    def testDamage(self):
        self.assertEqual(self.caedris.damageCode(), 7)

    def testMembership(self):
        scene = Scene.CombatScene([])
        self.assertEqual(len(scene.characters), 0)
        scene.addCharacter(self.caedris)
        scene.beginBattle()
        self.assertEqual(len(scene.battleWheel.activeCharacters), 1)
        scene.battleWheel.removeCharacter(self.caedris)
        self.assertEqual(len(scene.battleWheel.activeCharacters), 0)
        self.assertFalse(any([self.caedris in tick for tick in scene.battleWheel.tickLayout.values()]))

    def testBattleWheel(self):
        bw = Scene.BattleWheel([])
        bw.addCharacterToTick(self.caedris, 4)
        self.assertTrue(self.caedris in bw.tickLayout[4])


class CharacterTest(unittest.TestCase):
    import ExaltedCharacter
    c = ExaltedCharacter.ExaltedCharacter('Willow.ecg')
    skogur = ExaltedCharacter.ExaltedCharacter('WanderingVengefulLink.ecg')
    blix = ExaltedCharacter.ExaltedCharacter('Blixorthodon.ecg')
    gin = ExaltedCharacter.ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
    swift = ExaltedCharacter.ExaltedCharacter('WarrickSwiftColson.ecg')
    zaela = ExaltedCharacter.ExaltedCharacter('ZaelaPrismaticUnfoldingLotus.ecg')

    def testPrintAttributes(self):
        print self.c.name
        usefulStats = ['Charisma', 'Presence', 'Survival']

        for stat in usefulStats:
            print stat, ":", int(self.c.getStat(stat) or 0)
        self.assertRaises(KeyError, self.c.getStat, 'Computers')
        print "For 'Perception', 'Awareness' Roll", self.c.sumDicePool('Perception', 'Awareness'), "dice"

    def testDerivedStats(self):
        self.assertEqual(self.c['Essence'], 4)
        self.assertEqual(self.c.peripheralEssence, 44)
        self.assertEqual(self.c.personalEssence, 19)

    def testRunningOut(self):
        self.c.roll('Compassion', 'Dexterity')
        self.c.roll('Compassion', 'Dexterity')
        self.assertRaises(ValueError, self.c.roll, 'Compassion', 'Dexterity' )

    def testChooseWeapon(self):
        self.assertEqual(self.gin.armorStats['name'], 'Superheavy Plate (Artifact)')
        self.assertEqual(self.gin.weaponStats['name'], 'Grand Goremaul')

    def testChooseAttackSkill(self):
        self.assertEqual(self.blix.accuracy(), 13)
        self.blix.weaponStats = self.blix.parseWeapon('War_Boomerang')
        self.assertEqual(self.blix.accuracy(), 4) #this should be using Thrown, because of the thrown tag stat block under knife

    def testCustomArmor(self):
        self.skogur.armorStats = self.skogur.parseArmor('Moon-Face Breastplate')
        self.assertEqual(self.skogur.armorStats['name'], 'Moon-Face Breastplate')

    def testCraftSkillAndSoakStacking(self):
        self.assertEqual(self.swift.getStat('Craft'),4)
        self.assertEqual(self.swift.soak(), 11)
        self.assertEqual(self.swift.armorStats, self.swift.parseArmor('Chain_Shirt__Artifact_With_Silken_Armor'))

    def testDying(self):
        self.gin.flurryAttack(6, self.zaela, False) # We are assuming this kills Zaela
        self.assertTrue(self.zaela.isDying)
        for turn in range(self.zaela.dyingHealthLevels.permanent-1):
            self.zaela.refreshDV()
        self.assertRaises(ValueError, self.zaela.refreshDV)

    def testSocialAttack(self):
        wp = [self.swift.socialAttack(self.gin, None, True, True, True) for i in range(4)]
        self.assertGreater(max(wp), 0)

if __name__ == '__main__':
    unittest.main()
