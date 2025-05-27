from ui.actors.behaviour import Behaviour
from ui.actors.vectors import Vec2


class MoveBehavior(Behaviour):
    def move_left(self):
        self.actor.track.append(Vec2(-1, 0))

    def move_right(self):
        self.actor.track.append(Vec2(1, 0))

    def move_up(self):
        self.actor.track.append(Vec2(0, -1))

    def move_down(self):
        self.actor.track.append(Vec2(0, 1))
