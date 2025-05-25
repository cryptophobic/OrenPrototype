from ui.actors.actions import Actions as BaseActions
from ui.actors.vectors import Vec2

# TODO make it configurable
from map.battlefield import battlefield


class Actions(BaseActions):

    def move_left(self):
        self.__track.append(Vec2(-1, 0))

    def move_right(self):
        self.__track.append(Vec2(1, 0))

    def move_up(self):
        self.__track.append(Vec2(0, -1))

    def move_down(self):
        self.__track.append(Vec2(0, 1))

    def commit(self):
        while self.__track:
            velocity = self.__track.popleft()
            cell_coordinates = self.actor.body.coordinates + velocity
            cell = battlefield.get_cell(cell_coordinates)
            if cell.is_occupied() and self.actor.is_conflicting(cell.unit.actor):
                self.__track.clear()

