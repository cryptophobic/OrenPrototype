from typing import TypeVar, Generic, Self
from .actor.coordinate_holder import CoordinateHolder
from .actors_collection import ActorsCollection

V = TypeVar("V", bound=CoordinateHolder)

class CoordinateHoldersCollection(ActorsCollection[V]):
    def __init__(self, items: dict[str, V] | None = None):
        super().__init__(items or {})

    def get_blocking_actors(self, other: CoordinateHolder) -> Self:
        return CoordinateHoldersCollection(self.filter(lambda a: a.blocks(other)))

    def get_overlapping_actors(self, other: CoordinateHolder) -> Self:
        return CoordinateHoldersCollection(self.filter(lambda a: a.overlaps(other)))
