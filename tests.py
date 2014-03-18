__author__ = 'Josiah Seaman'
from TemporaryStat import RulesError
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
        self.assertFalse(any([self.caedris in tick for tick in list(scene.battleWheel.tickLayout.values())]))

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
    caedris = ExaltedCharacter.ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')

    def testPrintAttributes(self):
        print(self.c.name)
        usefulStats = ['Charisma', 'Presence', 'Survival']

        for stat in usefulStats:
            print(stat, ":", int(self.c.getStat(stat) or 0))
        self.assertRaises(KeyError, self.c.getStat, 'Computers')
        print("For 'Perception', 'Awareness' Roll", self.c.sumDicePool('Perception', 'Awareness'), "dice")

    def testDerivedStats(self):
        self.assertEqual(self.c['Essence'], 4)
        self.assertEqual(self.c.peripheralEssence, 44)
        self.assertEqual(self.c.personalEssence, 19)

    def testRunningOut(self):
        self.c.roll('Compassion', 'Dexterity')
        self.c.roll('Compassion', 'Dexterity')
        self.assertRaises(RulesError, self.c.roll, 'Compassion', 'Dexterity' )

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
        self.assertEqual(self.swift.soak(), 12)
        self.assertEqual(self.swift.armorStats, self.swift.parseArmor('Chain_Shirt__Artifact_With_Silken_Armor'))

    def testDying(self):
        self.gin.flurryAttack(6, self.zaela, False) # We are assuming this kills Zaela
        self.assertTrue(self.zaela.isDying)
        for turn in range(self.zaela.dyingHealthLevels.permanent-1):
            self.zaela.refreshDV()
        self.assertRaises(ValueError, self.zaela.refreshDV)

    def testSocialAttack(self):
        wp = []
        for i in range(4):
            wp.append(self.swift.socialAttack(self.gin, None, True, True, True))
            self.swift.refreshDV()
        self.assertGreater(max(wp), 0)
        self.assertEqual(self.blix.appearanceAdjustment(self.swift), -1)
        self.assertEqual(self.blix.adjustedMDV(self.swift, True, None, False), 6-1-3+1)#MDV - App -Motiv + Intimacy

    def testHandleAction(self):
        self.caedris.refreshDV()
        self.caedris.flurry(2)
        self.caedris.handleAction('Jump')
        self.caedris.handleAction('Dash')
        self.assertEqual(self.caedris.dvPenalty, -3)
        self.assertEqual(self.caedris.longestActionSpeed, 5)
        self.assertEqual(self.caedris.actionsRemaining.temporary, 0)
        self.assertRaises(RulesError, self.caedris.handleAction, 'Jump')

        self.caedris.refreshDV()
        self.caedris.flurry(3)
        self.caedris.handleAction('Jump', False)
        self.caedris.handleAction('Dash', False)
        self.assertEqual(self.caedris.dvPenalty, -2)
        self.assertEqual(self.caedris.longestActionSpeed, 5)
        self.assertEqual(self.caedris.actionsRemaining.temporary, 1)

    def testClinch(self):
        # scary char + huge DV penalty
        pass

class AnathemaParserTest(unittest.TestCase):
    from AnathemaParser import AnathemaParser
    ap = AnathemaParser('Willow.ecg')
    root = ap.root

    def testPase(self):
        result = self.ap.parse_to_dictionary()
        expected = {'Appearance': 4,
                    'Archery': 0,
                    'Athletics': 3,
                    'Awareness': 5,
                    'Bureaucracy': 0,
                    'Charisma': 5,
                    'Compassion': 2,
                    'Concept': 'Druid Sorceror',
                    'Conviction': 3,
                    'Craft': 0,
                    'Dexterity': 3,
                    'Dodge': 5,
                    'Equipment': ['Superheavy Plate (Artifact)',
                                  'Wood Dragon Claw (Offensive)',
                                  'Wood Dragon Claw (Defensive)'],
                    'Essence': 4,
                    'Integrity': 0,
                    'Intelligence': 4,
                    'Investigation': 0,
                    'Larceny': 0,
                    'Limit': 0,
                    'Linguistics': 0,
                    'Lore': 2,
                    'Manipulation': 2,
                    'MartialArts': 5,
                    'Medicine': 0,
                    'Melee': 0,
                    'Name': 'Willow',
                    'Occult': 5,
                    'Perception': 3,
                    'Performance': 1,
                    'Player': 'Corina',
                    'Presence': 3,
                    'Resistance': 1,
                    'Ride': 1,
                    'Sail': 0,
                    'Socialize': 1,
                    'Specialties': {'Occult': ('Forest', 3), 'Survival': ('Leading Groups', 1)},
                    'Stamina': 2,
                    'Stealth': 2,
                    'Strength': 2,
                    'Survival': 5,
                    'Temperance': 2,
                    'Thrown': 0,
                    'Type': 'Solar',
                    'Valor': 2,
                    'War': 0,
                    'Willpower': 7,
                    'Wits': 2}
        self.assertDictEqual(result, expected, )



if __name__ == '__main__':
    unittest.main()
