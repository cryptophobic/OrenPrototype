from collections import deque

from ui.actors.actor import Actor
from ui.actors.vectors import Vec2


class Actions:
    def __init__(self, actor: Actor):
        self.actor = actor
        self.__track: deque[Vec2] = deque()
        pass

    def commit(self):
        pass
