from ui.actors.actor import Actor
from ui.actors.cursor.actions import Actions
from ui.actors.cursor.controls import Controls


class Cursor(Actor):
    def __init__(self):
        super().__init__()
        self.actions = Actions(self)
        self.controls = Controls(self)