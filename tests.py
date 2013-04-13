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
        from Scene import *
        scene = CombatScene()
        caedris = ExaltedCharacter('Caedris.ecg')
        willow = ExaltedCharacter('Willow.ecg')
        scene.addCharacter(caedris)
        scene.addCharacter(willow)
        scene.beginScenario()
        print 'Done'

if __name__ == '__main__':
    unittest.main()
