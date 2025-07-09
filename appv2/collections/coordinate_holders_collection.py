from typing import TypeVar, Self

from appv2.collections.actors_collection import ActorsCollection
from appv2.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol

V = TypeVar("V", bound=CoordinateHolderProtocol)

class CoordinateHoldersCollection(ActorsCollection[V]):
    def __init__(self, items: dict[str, V] | None = None):
        super().__init__(items or {})

    def get_blocking_actors(self, other: CoordinateHolderProtocol) -> Self:
        return CoordinateHoldersCollection(self.filter(lambda a: a.blocks(other)))

    def get_overlapping_actors(self, other: CoordinateHolderProtocol) -> Self:
        return CoordinateHoldersCollection(self.filter(lambda a: a.overlaps(other)))

    @classmethod
    def from_collections(cls, collections: list[Self]) -> Self:
        merged = {}
        for collection in collections:
            merged.update(collection.items())
        return cls(merged)
