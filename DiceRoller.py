import random

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


def skillCheckByNumber(nDice, label=None):
    if not label: label = "Skill"
    rolls = roll(nDice, label)
    hits = filter(lambda x: x >= 7, rolls)
    tens = rolls.count(10)
    successes = len(hits) + tens
    if not successes and rolls.count(1):
        print "BOTCH!"
    return successes


def s(nDice):
    return skillCheckByNumber(nDice)


def toHit(accuracy, DV):
    hits = skillCheckByNumber(accuracy, "Attack")
    threshold = -1
    if hits < DV:
        print "You missed"
    else:
        threshold = hits - DV
        print threshold, "successes over a DV of", DV
    return threshold


def toDamage(damageCode, hardness, minimumDamage, soak, thresholdToHit):
    if damageCode + thresholdToHit <= hardness:
        print "Didn't beat hardness", hardness
    else:
        damageDice = max(damageCode + thresholdToHit - soak, minimumDamage)
        damageDone = rollDamage(damageDice) or 0
        print "Take", damageDone, "out of", damageDice, "damage dice."
    return damageDone


def attackRoll(accuracy, damageCode, DV, soak, hardness=0, minimumDamage=1):
    threshold = toHit(accuracy, DV)
    damageDone = 0
    if threshold > -1:
        damageDone = toDamage(damageCode, hardness, minimumDamage, soak, threshold)
    return damageDone


def flurry(nAttacks, accuracy, damageCode, DV, soak, hardness=0, minimumDamage=1, hasPenalty=True ):
    penalties = range( nAttacks-1, (nAttacks-1)+nAttacks) if hasPenalty else [0]*nAttacks
    damageDone = []
    for onslaught, penalty in enumerate(penalties):
        damageDone.append(attackRoll(accuracy-penalty, damageCode, max(0, DV-onslaught), soak, hardness, minimumDamage))
    print "Total damage done:", sum(damageDone)
    return sum(damageDone)


def outcomePlot(nDice):
    record = {}
    for i in range(1000):
        score = s(nDice)
        record[score] = 1 + record.get(score, 0)

    for score, height in record.iteritems():
        print score, '.' * height
