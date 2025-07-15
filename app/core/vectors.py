from dataclasses import dataclass
import math

from app.config import Y_MODIFIER


@dataclass
class CustomVec2:
    x: int
    y: int

    X = 0
    Y = 1

    @staticmethod
    def up(magnitude: int = 1):
        return CustomVec2(0, -magnitude * Y_MODIFIER)

    @staticmethod
    def down(magnitude: int = 1):
        return CustomVec2(0, magnitude * Y_MODIFIER)

    @staticmethod
    def left(magnitude: int = 1):
        return CustomVec2(-magnitude, 0)

    @staticmethod
    def right(magnitude: int = 1):
        return CustomVec2(magnitude, 0)

    def __getitem__(self, item: int) -> int:
        if item > 1:
            raise IndexError("Out of range of 2 dimensional vector")

        return (self.x, self.y)[item]

    def __add__(self, other):
        return CustomVec2(self.x + other[CustomVec2.X], self.y + other[CustomVec2.Y])

    def __sub__(self, other):
        return CustomVec2(self.x - other[CustomVec2.X], self.y - other[CustomVec2.Y])

    def __neg__(self):
        return CustomVec2(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def is_zero(self):
        return self.x == self.y == 0

    def is_not_zero(self) -> bool:
        return self.x != 0 or self.y != 0

    def iterate_to(self, other):
        return iterate_path(self, other)

    def iterate_from(self, other):
        return iterate_path(other, self)

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def scalar_multiply(self, scalar):
        return CustomVec2(int(self.x * scalar), int(self.y * scalar))


def iterate_path(from_vec: CustomVec2, to_vec: CustomVec2):
    incr = CustomVec2(1 if to_vec.x > from_vec.x else -1, 1 if to_vec.y > from_vec.y else -1)
    res = CustomVec2(from_vec.x, from_vec.y)

    while res != to_vec:
        if res.x != to_vec.x:
            res.x += incr.x
            yield res

        if res.y != to_vec.y:
            res.y += incr.y
            yield res
