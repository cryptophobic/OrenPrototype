from typing import Self, TypeVar

from .actor.static_object import StaticObject
from .coordinate_holders_collection import CoordinateHoldersCollection

T = TypeVar("T", bound=StaticObject)

class StaticObjectsCollection(CoordinateHoldersCollection[T]):
    def __init__(self, items: dict[str, T] | None = None):
        super().__init__(items or {})

    def get_taller_than(self, height, inclusive = False) -> Self:
        return type(self)(self.filter(lambda a: a.height >= height if inclusive else a.height > height))

    def get_shorter_than(self, height, inclusive = False) -> Self:
        return type(self)(self.filter(lambda a: a.height <= height if inclusive else a.height < height))

    def get_with_height(self, height) -> Self:
        return type(self)(self.filter(lambda a: a.height == height))
