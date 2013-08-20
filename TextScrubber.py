import re

"""This was a quick script to get the glossary of terms used in the character sheet"""

# f = open('CaedrisEmissaryofTenThousandWinds.ecg')
# for line in f:
#     tokens = re.split(' |<|>|=', line)
#
#     # print tokens
#     for index, word in enumerate(tokens):
#         if word == 'creationValue':
#             r = tokens[index-1]
#             if r in ['subTrait', 'Trait', 'Background']: continue #ignore these tokens
#             print r.lower(), "=", "'" + r + "'"


spec = [("Attack", None, -1),  # None means that it varies, as opposed to -0 DV penalty
        ("Clinch", 6, -10),  # I think you lose your DV against others when you clinch someone
        ("Guard", 3, 0),  # Holding Action
        ("Aim", 3, -1),  # Holding Action
        ("Ready Weapon", 5, 0),
        ("Performance", 6, -2),
        ("Presence", 4, -2),
        ("Investigation", 5, -2),
        ("Coordinate Attack", 5, 0),
        ("Simple Charm", 6, -1),
        ("Defend Other", 5, 0),
        ("Dash", 3, -2),
        ("Jump", 5, -1),
        ("Rise from Prone", 5, -1),
        ("Miscellaneous", 5, -1),
        ("Inactive", 5, -20)]

for action in spec:
    print action[0].lower(), "= '" +action[0] +"'"