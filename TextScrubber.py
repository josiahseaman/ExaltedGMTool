import re

"""This was a quick script to get the glossary of terms used in the character sheet"""

f = open('CaedrisEmissaryofTenThousandWinds.ecg')
for line in f:
    tokens = re.split(' |<|>|=', line)

    # print tokens
    for index, word in enumerate(tokens):
        if word == 'creationValue':
            r = tokens[index-1]
            if r in ['subTrait', 'Trait', 'Background']: continue #ignore these tokens
            print r.lower(), "=", "'" + r + "'"
