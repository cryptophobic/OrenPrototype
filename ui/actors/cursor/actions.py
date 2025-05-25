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

    def commit(self, coordinates: Vec2):
        while self.__track:
            velocity = self.__track[0]
            cell_coordinates = coordinates + velocity
            cell = battlefield.get_cell(cell_coordinates)
            if cell.is_occupied():
                body = cell.unit.actor.body
                if body.is_solid() or body.is_soft():
                    return False, coordinates,

            self.__track.popleft()
            coordinates += velocity

        return True, coordinates

