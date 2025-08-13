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

    @staticmethod
    def _cast(v):  # overridden in subclasses
        return v

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

@dataclass(frozen=True, slots=True)
class Vec2Ops(VecBase, Generic[T]):

    def with_x(self, x: T) -> Self:
        return type(self)(self._cast(x), self.y)

    def with_y(self, y: T) -> Self:
        return type(self)(self.x, self._cast(y))

    def with_index(self, i: int, value: T) -> Self:
        if i == 0: return type(self)(self._cast(value), self.y)
        if i == 1: return type(self)(self.x, self._cast(value))
        raise IndexError("Vec2 index must be 0 or 1")

    def update(self, *, x: T | None = None, y: T | None = None) -> Self:
        # kwargs-only to prevent accidental positional misuse
        return type(self)(
            self._cast(self.x if x is None else x),
            self._cast(self.y if y is None else y),
        )

    def __getitem__(self, i: int) -> T:
        if i == 0: return self.x
        if i == 1: return self.y
        raise IndexError("Vec2 index must be 0 or 1")

    def __add__(self, other: Self) -> Self:
        return type(self)(self._cast(self.x + other.x), self._cast(self.y + other.y))

    def __sub__(self, other: Self) -> Self:
        return type(self)(self._cast(self.x - other.x), self._cast(self.y - other.y))

    def __mul__(self, n: T) -> Self:
        return type(self)(self._cast(self.x * n), self._cast(self.y * n))

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Self) -> bool:
        return self.x != other.x or self.y != other.y

    def add(self, other: Self) -> Self:
        return type(self)(self._cast(self.x + other.x), self._cast(self.y + other.y))
    def sub(self, other: Self) -> Self:
        return type(self)(self._cast(self.x - other.x), self._cast(self.y - other.y))
    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y
    def mag(self) -> float:
        return math.hypot(self.x, self.y)

    def is_zero(self) -> bool:
        return self.x == 0 and self.y == 0
    def is_not_zero(self) -> bool:
        return not self.is_zero()


@dataclass(frozen=True, slots=True)
class CustomVec2f(Vec2Ops[float]):

    x: float
    y: float

    @staticmethod
    def _cast(v) -> float: return float(v)

    def normalized(self) -> Self:
        m = self.mag()
        return CustomVec2f(0.0, 0.0) if m == 0 else CustomVec2f(self.x/m, self.y/m)

@dataclass(frozen=True, slots=True)
class CustomVec2i(Vec2Ops[int]):
    x: int
    y: int

    @staticmethod
    def _cast(v) -> int: return int(v)
