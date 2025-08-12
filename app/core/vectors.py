from dataclasses import dataclass
from typing import Generic, TypeVar, Self
from numbers import Real

from app.config import Y_MODIFIER

T = TypeVar("T", bound=Real)

from typing import Self
import math

@dataclass(frozen=True, slots=True)
class VecBase(Generic[T]):
    x: T
    y: T

    # All these methods use cls(...) so the returned object matches the subclass.
    @classmethod
    def up(cls, m: T = 1) -> Self:
        return cls(cls._cast(0), cls._cast(-m * Y_MODIFIER))

    @classmethod
    def down(cls, m: T = 1) -> Self:
        return cls(cls._cast(0), cls._cast(m * Y_MODIFIER))

    @classmethod
    def left(cls, m: T = 1) -> Self:
        return cls(cls._cast(-m), cls._cast(0))

    @classmethod
    def right(cls, m: T = 1) -> Self:
        return cls(cls._cast(m), cls._cast(0))

    @classmethod
    def zero(cls) -> Self:
        return cls(cls._cast(0), cls._cast(0))

    @staticmethod
    def _cast(value) -> T:
        # Override in subclasses if you want strict type conversion
        return value


@dataclass(frozen=True, slots=True)
class Vec2Ops(VecBase, Generic[T]):

    def __getitem__(self, item: int) -> T:
        if item > 1:
            raise IndexError("Out of range of 2 dimensional vector")

        return (self.x, self.y)[item]

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, n: T) -> Self:
        return type(self)(self.x * n, self.y * n)

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Self) -> bool:
        return self.x != other.x or self.y != other.y

    def add(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def sub(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)
    def neg(self) -> Self:
        return type(self)(-self.x, -self.y)
    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y
    def mag(self) -> float:
        return math.hypot(self.x, self.y)


@dataclass(frozen=True, slots=True)
class CustomVec2f(Vec2Ops[float]):

    def normalized(self) -> Self:
        m = self.mag()
        return CustomVec2f(0.0, 0.0) if m == 0 else CustomVec2f(self.x/m, self.y/m)

@dataclass(frozen=True, slots=True)
class CustomVec2i(Vec2Ops[int]):
    pass
