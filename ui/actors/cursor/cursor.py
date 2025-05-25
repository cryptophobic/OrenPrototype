from ui.actors.actor import Actor
from ui.actors.cursor.actions import Actions
from ui.actors.cursor.body import Body
from ui.actors.cursor.controls import Controls
from ui.actors.vectors import Vec2


class Cursor(Actor):
    def __init__(self, coordinates: Vec2):
        super().__init__(coordinates)
        self.actions = Actions()
        self.controls = Controls(self.actions)
        self.body = Body()