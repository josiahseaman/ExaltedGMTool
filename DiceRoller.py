import random

random.seed()


def roll(nDice, label=None):
    x = [random.randrange(1, 11) for i in range(nDice)]
    x = sorted(x,reverse=True)
    if label:
        print(label, x)
    return x


def rollDamage(nDice):
    rolls = roll(nDice, "Damage:")
    hits = [x for x in rolls if x >= 7]
    return len(hits)


def d(nDice):
    return rollDamage(nDice)


def skillCheckByNumber(nDice, label=None, difficulty=0):
    if not label: label = "Skill"
    rolls = roll(nDice, label)
    hits = [x for x in rolls if x >= 7]
    tens = rolls.count(10)
    successes = len(hits) + tens
    if not successes and rolls.count(1):
        print("BOTCH!")
        successes = -1
    if difficulty:
        threshold = successes - difficulty
        if successes < difficulty:
            print("You fail at", label)
        else:
            print("You succeed at", label, "with", threshold, "threshold successes.")
        successes = threshold
    return successes


def s(nDice):
    return skillCheckByNumber(nDice)


def toHit(accuracy, DV):
    threshold = skillCheckByNumber(accuracy, "Attack", DV)
    return threshold


def toDamage(damageCode, hardness, soak, thresholdToHit=0, minimumDamage=1):
    if damageCode + thresholdToHit <= hardness:
        print("Didn't beat hardness", hardness)
    else:
        damageDice = max(damageCode + thresholdToHit - soak, minimumDamage)
        damageDone = rollDamage(damageDice) or 0
        print("Take", damageDone, "out of", damageDice, "damage dice.")
    return damageDone


def attackRoll(accuracy, damageCode, DV, soak, hardness=0, minimumDamage=1):
    threshold = toHit(accuracy, DV)
    damageDone = 0
    if threshold > -1:
        damageDone = toDamage(damageCode, hardness, soak, threshold, minimumDamage)
    return damageDone


def flurry(nAttacks, accuracy, damageCode, DV, soak, hardness=0, minimumDamage=1, hasPenalty=True ):
    penalties = list(range( nAttacks-1, (nAttacks-1)+nAttacks)) if hasPenalty else [0]*nAttacks
    damageDone = []
    for onslaught, penalty in enumerate(penalties):
        damageDone.append(attackRoll(accuracy-penalty, damageCode, max(0, DV-onslaught), soak, hardness, minimumDamage))
    print("Total damage done:", sum(damageDone))
    return sum(damageDone)


def outcomePlot(nDice):
    record = {}
    for i in range(1000):
        score = s(nDice)
        record[score] = 1 + record.get(score, 0)

    for score, height in record.items():
        print(score, '.' * height)
