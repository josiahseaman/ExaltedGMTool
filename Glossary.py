import copy
from ExaltedCharacter import ExaltedCharacter
import Scene


alatu = ExaltedCharacter('AlatutheForsaken.ecg')
amod = ExaltedCharacter('Amod.ecg')
quinn = ExaltedCharacter('QuinnLanus.ecg')
qismet = ExaltedCharacter('Qismet.ecg')
storm = ExaltedCharacter('BlindingStorm.ecg')
gray = ExaltedCharacter('LordVarys.ecg')

# load_masteries
alatu.masteries = {"Melee":2,
"Occult":3,
"Presence":2}

amod.masteries = {"Athletics":1,
"Melee":3,
"Occult":3,
"Resistance":1,
"Stealth":2,
"Thrown":3,}

quinn.masteries = {"Bureaucracy":1,
"Presence":2,
"Linguistics":2,
"Craft":3,
"Lore":3,
"Investigation":2,
"Martial Arts":2}

qismet.masteries = {"Athletics":1,
"Awareness":3,
"Dodge":3,
"Investigation":2,
"Melee":2,
"Occult":2,
"Stealth":2}

storm.masteries = {"Investigation":2,
"Martial Arts":1,
"Occult":3,
"Resistance":3}

gray.masteries = {"Awareness":2,
"Integrity":2,
"Investigation":3,
"Martial Arts":2,
"Occult":2}

PlayerCharacters = [alatu, amod, quinn, qismet, storm, gray]
NPCs = []
names = ['alatu', 'amod', 'quinn', 'qismet', 'storm', 'gray']
for index, pc in enumerate(PlayerCharacters):
    evil_pc = copy.deepcopy(pc)
    evil_pc.name = "Evil " + evil_pc.name
    locals()['evil_'+names[index]] = evil_pc
    NPCs.append(evil_pc)

sc = Scene.CombatScene(PlayerCharacters + NPCs)


def c():
    return sc.current


essence = 'Essence'
willpower = 'Willpower'
compassion = 'Compassion'
conviction = 'Conviction'
temperance = 'Temperance'
valor = 'Valor'
strength = 'Strength'
dexterity = 'Dexterity'
dex = 'Dexterity'
stamina = 'Stamina'
charisma = 'Charisma'
manipulation = 'Manipulation'
appearance = 'Appearance'
perception = 'Perception'
intelligence = 'Intelligence'
wits = 'Wits'
craft = 'Craft'
archery = 'Archery'
martialarts = 'MartialArts'
MA = 'MartialArts'
melee = 'Melee'
thrown = 'Thrown'
war = 'War'
integrity = 'Integrity'
performance = 'Performance'
presence = 'Presence'
resistance = 'Resistance'
survival = 'Survival'
investigation = 'Investigation'
lore = 'Lore'
medicine = 'Medicine'
occult = 'Occult'
athletics = 'Athletics'
awareness = 'Awareness'
dodge = 'Dodge'
larceny = 'Larceny'
stealth = 'Stealth'
bureaucracy = 'Bureaucracy'
linguistics = 'Linguistics'
ride = 'Ride'
sail = 'Sail'
socialize = 'Socialize'
limit = 'Limit'

#Actions
attack = 'Attack'
clinch = 'Clinch'
guard = 'Guard'
aim = 'Aim'
draw = 'Ready Weapon'
perform = 'Performance'
presence = 'Presence'
miscellaneous = 'Miscellaneous'
inactive = 'Inactive'
investigate = 'Investigation'
coordinate = 'Coordinate Attack'
simple = 'Simple Charm'
defend = 'Defend Other'
dash = 'Dash'
jump = 'Jump'
rise = 'Rise from Prone'
blockade = 'Blockade Movement'
shape = "Shape Sorcery"

# swift = ExaltedCharacter('WarrickSwiftColson.ecg')
# gin = ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
# # caedris = ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')
# caedin = ExaltedCharacter('CaidenUnionofWanderedStars.ecg')
# zaela = ExaltedCharacter('ZaelaPrismaticUnfoldingLotus.ecg')
# blix = ExaltedCharacter('Blixorthodon.ecg')
# skogur = ExaltedCharacter('WanderingVengefulLink.ecg')
# willow = ExaltedCharacter('Willow.ecg')
# arc = ExaltedCharacter('Arczeckhi.ecg')
# neph = ExaltedCharacter('Nephwrack.ecg')
# zombie = ExaltedCharacter('Zombie.ecg')

