from Glossary import *
import Scene

__author__ = 'Josiah'

class UI():
    def __init__(self):
        self.scene = Scene.CombatScene(PlayerCharacters)
        self.scene.beginBattle()

    def start(self):
        while True:
            actor = self.scene.battleWheel.nextAction()
            speed = self.promptUser(actor) #do stuff
            self.scene.battleWheel.resolveAction(speed)

    def promptUser(self, actor):
        print actor.name, "is ready"
        speed = input("Speed:")
        return speed

if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="
    gt = UI()
    print "New combat scene created containing: ", gt.scene.characters.values()
    gt.start()

