from ElementTree import *


class ExaltedCharacter():

    def parse(self):
        filename = 'Willow.ecg'
        tree = ElementTree(file=filename)
        # the tree root is the toplevel html element
        print tree.findtext("ExaltedCharacter")

        # if you need the root element, use getroot
        root = tree.getroot()
        print tostring(root)
        #for text in root.itertext():
        #    print repr(text)
        print getText(root)

    def __init__(self):
        self.accuracy = 1
        self.damageCode = 1
        self.DV = 1
        self.soak = 1

def getText(elem):
    return "".join(elem.itertext())
    
if __name__ == "__main__":
    c = ExaltedCharacter()
    c.parse()
