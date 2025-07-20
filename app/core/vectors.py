from dataclasses import dataclass
from typing import Generic, TypeVar

from app.config import Y_MODIFIER

T = TypeVar("T")  # Value type — e.g. int, float.

@dataclass
class CustomVec2(Generic[T]):
    x: T
    y: T

    X = 0
    Y = 1

    @staticmethod
    def up(magnitude: T = 1):
        return CustomVec2(0, -magnitude * Y_MODIFIER)

    @staticmethod
    def down(magnitude: T = 1):
        return CustomVec2(0, magnitude * Y_MODIFIER)

    @staticmethod
    def left(magnitude: T = 1):
        return CustomVec2(-magnitude, 0)

    @staticmethod
    def right(magnitude: T = 1):
        return CustomVec2(magnitude, 0)

    @staticmethod
    def zero(magnitude: T = 1):
        return CustomVec2(magnitude, 0)

    def __getitem__(self, item: int) -> T:
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

    def length(self) -> T:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def scalar_multiply(self, scalar):
        return CustomVec2(int(self.x * scalar), int(self.y * scalar))


@dataclass
class CustomVec2i(CustomVec2[int]):
    def to_float(self) -> 'CustomVec2f':
        return CustomVec2f(float(self.x), float(self.y))

    def manhattan_distance(self, other: 'CustomVec2i') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class CustomVec2f(CustomVec2[float]):
    def to_int(self) -> 'CustomVec2i':
        return CustomVec2i(int(self.x), int(self.y))

