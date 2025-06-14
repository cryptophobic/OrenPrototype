from typing import TypeVar, Generic
from .actor.coordinate_holder import CoordinateHolder
from .actors_collection import ActorsCollection

T = TypeVar("T", bound=CoordinateHolder)

class CoordinateHoldersCollection(ActorsCollection[T], Generic[T]):
    def __init__(self, items: dict[str, T] | None = None):
        super().__init__(items or {})

    def get_blocking_actors(self, other: CoordinateHolder) -> 'CoordinateHoldersCollection':
        return CoordinateHoldersCollection(self.filter(lambda a: a.blocks(other)))

    def get_overlapping_actors(self, other: CoordinateHolder) -> 'CoordinateHoldersCollection':
        return CoordinateHoldersCollection(self.filter(lambda a: a.overlaps(other)))
