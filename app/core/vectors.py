import math
from dataclasses import dataclass
from typing import Generic, TypeVar, Self

from app.config import Y_MODIFIER

T = TypeVar("T")  # Value type — e.g. int, float.

@dataclass
class CustomVec2(Generic[T]):
    x: T
    y: T

    X = 0
    Y = 1

    @classmethod
    def up(cls, magnitude: T = 1):
        return cls(0, -magnitude * Y_MODIFIER)

    @classmethod
    def down(cls, magnitude: T = 1):
        return cls(0, magnitude * Y_MODIFIER)

    @classmethod
    def left(cls, magnitude: T = 1):
        return cls(-magnitude, 0)

    @classmethod
    def right(cls, magnitude: T = 1):
        return cls(magnitude, 0)

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def copy(self):
        return type(self)(self.x, self.y)

    def __getitem__(self, item: int) -> T:
        if item > 1:
            raise IndexError("Out of range of 2 dimensional vector")

        return (self.x, self.y)[item]

    def __add__(self, other):
        return type(self)(self.x + other[CustomVec2.X], self.y + other[CustomVec2.Y])

    def __sub__(self, other):
        return type(self)(self.x - other[CustomVec2.X], self.y - other[CustomVec2.Y])

    def __mul__(self, n: T):
        return type(self)(self.x * n, self.y * n)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def is_zero(self):
        return self.x == self.y == 0

    def is_not_zero(self) -> bool:
        return self.x != 0 or self.y != 0

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def scalar_multiply(self, scalar):
        return type(self)(int(self.x * scalar), int(self.y * scalar))


@dataclass
class CustomVec2i(CustomVec2[int]):
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def to_float(self) -> 'CustomVec2f':
        return CustomVec2f(float(self.x), float(self.y))

    def manhattan_distance(self, other: 'CustomVec2i') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def normalized(self) -> Self:
        l = self.length()
        if l == 0:
            return CustomVec2f(0.0, 0.0)
        return CustomVec2f(self.x / l, self.y / l)


@dataclass
class CustomVec2f(CustomVec2[float]):

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    def to_int(self) -> Self:
        return CustomVec2i(int(self.x), int(self.y))

    def normalized(self) -> Self:
        l = self.length()
        if l == 0:
            return CustomVec2f(0.0, 0.0)
        return CustomVec2f(self.x / l, self.y / l)

    def scale_to(self, magnitude: float) -> Self:
        return self.normalized() * magnitude

def angle_to_vector(degrees: float):
    radians = math.radians(degrees)
    return CustomVec2f(math.cos(radians), math.sin(radians))

def vector_to_angle(start: CustomVec2, end: CustomVec2) -> float:
    dx = end.x - start.x
    dy = end.y - start.y
    return math.degrees(math.atan2(dy, dx))  # returns angle in degrees

def point_in_sector_dot(point: CustomVec2f, origin: CustomVec2f, facing_dir: CustomVec2f, cone_angle_deg, radius):
    delta: CustomVec2f = point - origin
    distance_squared = delta.x * delta.x + delta.y * delta.y
    if distance_squared > radius * radius:
        return False

    len_v = math.sqrt(distance_squared)
    if len_v == 0:
        return True  # target is at the origin

    # Normalize V (vector to point)
    vector_to_point: CustomVec2f = delta * (1/len_v)

    # Compute cosine of angle between V and facing_dir
    dot = vector_to_point.x * facing_dir.x + vector_to_point.y * facing_dir.y

    # Precompute cosine of half the cone angle
    cos_half_angle = math.cos(math.radians(cone_angle_deg / 2))
    return dot >= cos_half_angle
