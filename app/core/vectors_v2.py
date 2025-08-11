from collections import namedtuple
from typing import Generic, TypeVar

from app.config import Y_MODIFIER

LightVec2 = namedtuple("LightCustomVec2", ["x", "y"])

T = TypeVar("T")

class Vec2Transform(Generic[T]):

    @staticmethod
    def up(magnitude: T = 1):
        return LightVec2(0, -magnitude * Y_MODIFIER)

    @staticmethod
    def down(magnitude: T = 1):
        return LightVec2(0, magnitude * Y_MODIFIER)