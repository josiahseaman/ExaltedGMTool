import ExaltedCharacter
import Scene

swift = ExaltedCharacter.ExaltedCharacter('WarrickSwiftColson.ecg')
gin = ExaltedCharacter.ExaltedCharacter('GintheFearlessRadianceofAwesomeHonor.ecg')
# caedris = ExaltedCharacter.ExaltedCharacter('CaedrisEmissaryofTenThousandWinds.ecg')
caedin = ExaltedCharacter.ExaltedCharacter('CaidenUnionofWanderedStars.ecg')
zaela = ExaltedCharacter.ExaltedCharacter('ZaelaPrismaticUnfoldingLotus.ecg')
blix = ExaltedCharacter.ExaltedCharacter('Blixorthodon.ecg')
skogur = ExaltedCharacter.ExaltedCharacter('WanderingVengefulLink.ecg')
willow = ExaltedCharacter.ExaltedCharacter('Willow.ecg')

arc = ExaltedCharacter.ExaltedCharacter('Arczeckhi.ecg')
neph = ExaltedCharacter.ExaltedCharacter('Nephwrack.ecg')
zombie = ExaltedCharacter.ExaltedCharacter('Zombie.ecg')

PlayerCharacters = [swift, gin, caedin, zaela, blix, skogur, willow]
sc = Scene.CombatScene(PlayerCharacters)

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


