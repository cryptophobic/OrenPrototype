from collections import deque

from deprecated.ui.actors.vectors import Vec2


class Actions:
    def __init__(self):
        self.__track: deque[Vec2] = deque()
        pass

    def current_velocity(self) -> Vec2:
        return self.__track[0] if self.__track else Vec2(0, 0)

    def clear_velocity(self):
        if self.__track:
            self.__track[0] = Vec2(0, 0)

    def commit(self, coordinates: Vec2):
        pass
