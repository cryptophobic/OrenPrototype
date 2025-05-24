from ui.actors.actor import Actor
from ui.actors.vectors import Vec2


class Actions:
    def __init__(self, actor: Actor):
        self.actor = actor
        pass

    def commit(self):
        self.actor.body.velocity = Vec2(0, 0)
        pass
