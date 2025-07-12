from typing import TypeVar, Self

from app.collections.actors_collection import ActorsCollection
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol

V = TypeVar("V", bound=CoordinateHolderProtocol)

class CoordinateHoldersCollection(ActorsCollection[V]):
    def get_blocking_actors(self, other: CoordinateHolderProtocol) -> Self:
        return self.filter(lambda a: a.blocks(other))

    def get_overlapping_actors(self, other: CoordinateHolderProtocol) -> Self:
        return self.filter(lambda a: a.overlaps(other))

    @classmethod
    def from_collections(cls, collections: list[Self]) -> Self:
        merged: dict[str, V] = {}
        for collection in collections:
            merged.update(collection.raw_items())
        return cls(merged)
