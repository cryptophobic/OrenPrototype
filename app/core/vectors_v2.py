from dataclasses import dataclass
from typing import Generic, TypeVar, Self
from numbers import Real

T = TypeVar("T", bound=Real)

@dataclass(frozen=True, slots=True)
class CustomVec2(Generic[T]):
    x: T
    y: T

    def add(self, other: "CustomVec2[T]") -> "CustomVec2[T]":
        return CustomVec2(self.x + other.x, self.y + other.y)

    def sub(self, other: "CustomVec2[T]") -> "CustomVec2[T]":
        return CustomVec2(self.x - other.x, self.y - other.y)

    def mul(self, n: T) -> "CustomVec2[T]":
        return type(self)(self.x * n, self.y * n)

    def neg(self) -> Self:
        return type(self)(-self.x, -self.y)

    def dot(self, o: "CustomVec2[T]") -> float:
        return self.x * o.x + self.y * o.y

    def mag(self) -> float:
        return (self.x*self.x + self.y*self.y) ** 0.5

    def normalized(self) -> "CustomVec2[float]":
        m = self.mag()
        return type(self)(0.0, 0.0) if m == 0 else type(self)(self.x/m, self.y/m)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, n: T) -> "CustomVec2[T]":
        return type(self)(self.x * n, self.y * n)

    def __neg__(self) -> Self:
        return type(self)(-self.x, -self.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y
