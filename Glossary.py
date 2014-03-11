from ExaltedCharacter import ExaltedCharacter
import Scene

# swift = ExaltedCharacter('WarrickSwiftColson.ecg')
# gin = ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
# # caedris = ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')
# caedin = ExaltedCharacter('CaidenUnionofWanderedStars.ecg')
# zaela = ExaltedCharacter('ZaelaPrismaticUnfoldingLotus.ecg')
# blix = ExaltedCharacter('Blixorthodon.ecg')
# skogur = ExaltedCharacter('WanderingVengefulLink.ecg')
# willow = ExaltedCharacter('Willow.ecg')
alatu = ExaltedCharacter('AlatutheForsaken.ecg')
amod = ExaltedCharacter('Amod.ecg')
quinn = ExaltedCharacter('QuinnLanus.ecg')
qismet = ExaltedCharacter('Qismet.ecg')
storm = ExaltedCharacter('BlindingStorm.ecg')

arc = ExaltedCharacter('Arczeckhi.ecg')
neph = ExaltedCharacter('Nephwrack.ecg')
zombie = ExaltedCharacter('Zombie.ecg')

PlayerCharacters = [alatu, amod, quinn, qismet, storm]
    # [swift, gin, caedin, zaela, blix, skogur, willow]
sc = Scene.CombatScene(PlayerCharacters)


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

