import Scene

__author__ = 'Josiah'

class UI():
    def __init__(self):
        self.scene = Scene.CombatScene(True)
        self.beginBattle()

    def next(self):
        while True:
            actor = self.scene.battleWheel.nextAction()
            speed = self.promptUser(actor)#do stuff
            self.scene.battleWheel.resolveAction(speed)

    def promptUser(self, actor):
        print actor.name, "is ready"
        return 6


