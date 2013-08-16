from Glossary import *
import Scene
from ExaltedCharacter import actions

__author__ = 'Josiah'


class UI():
    def __init__(self):
        self.scene = Scene.CombatScene(PlayerCharacters)
        self.scene.beginBattle()

    def start(self):
        while True:
            actor = self.scene.battleWheel.getCurrentCharacter()
            # speed = self.promptUser(actor) #do stuff

            self.scene.battleWheel.moveCurrentCharacterForward(speed)

    def walkUserThroughParameters(self, actor, func):
        try:
            actionSpeed = func(actor) # call function
        except:
            target = mook #TODO: user inputs target character
            actionSpeed = func(actor, target)
        return actionSpeed

    def promptUser(self, actor):
        for index, action in enumerate(actions):
            print str(index+1) + ")", action
        print actor.name, "is ready"
        actionNumber = input("Speed:") - 1
        declaredAction = actions[actionNumber][1] #figure out which action

        actionSpeed = self.walkUserThroughParameters(actor, declaredAction)

        defaultSpeed = actions[actionNumber][2]
        speed = actionSpeed if defaultSpeed is None else defaultSpeed # if defaultSpeed is specified, use that over actionSpeed
        return speed

if __name__ == '__main__':
    print "==Exalted GM Assistant Activated=="
    gt = UI()
    print "New combat scene created containing: ", gt.scene.characters.values()
    gt.start()

