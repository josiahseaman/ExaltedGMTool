import random
from ExaltedCharacter import ExaltedCharacter

random.seed()

def roll(nDice, label=None):
   x = [random.randrange(1,11) for i in range(nDice)]
   x = sorted(x,reverse=True)
   if label:
      print label, x
   return x

def rollDamage(nDice):
   rolls = roll(nDice, "Damage:")
   hits = filter(lambda x: x >= 7, rolls)
   return len(hits)

def d(nDice):
   return rollDamage(nDice)

def skillCheck(nDice, label=None):
   if not label: label = "Skill:"
   rolls = roll(nDice, label)
   hits = filter(lambda x: x >= 7, rolls)
   tens = rolls.count(10)
   successes = len(hits) + tens
   if not successes and rolls.count(1):
      print "BOTCH!"
   return successes

def s(nDice):
   return skillCheck(nDice)

def attack(accuracy, damageCode, DV, soak):
   hits = skillCheck(accuracy, "Attack")
   if hits < DV:
      print "You missed"
      return 0 
   threshold = hits - DV
   print threshold, "successes over a DV of", DV
   damageDice = max(damageCode + threshold - soak, 1)
   damageDone = rollDamage(damageDice) or 0
   print "Take", damageDone, "out of", damageDice, "damage dice."
   return damageDone

def flurry(nAttacks, accuracy, damageCode, DV, soak):
   penalties = range( nAttacks-1, (nAttacks-1)+nAttacks)
   damageDone = []
   for penalty in penalties:
      damageDone.append(attack(accuracy-penalty, damageCode, DV, soak))
   print "Total damage done:", sum(damageDone)
   return sum(damageDone)

def characterFlurryAttack(nAttacks, attackingChar, defendingChar):
   return flurry(nAttacks, attackingChar.accuracy, attackingChar.damageCode, defendingChar.DV, defendingChar.soak)

def testScene(nAttacks=3):
   dace = ExaltedCharacter()
   swift = ExaltedCharacter()
   characterFlurryAttack(nAttacks, dace, swift)


print "==Exalted GM Assistant Activated=="
