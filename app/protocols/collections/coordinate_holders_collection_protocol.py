from typing import Protocol, Self, TypeVar, runtime_checkable
from app.protocols.collections.actors_collection_protocol import ActorsCollectionProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol

V = TypeVar("V", bound=CoordinateHolderProtocol)

@runtime_checkable
class CoordinateHoldersCollectionProtocol(ActorsCollectionProtocol[V], Protocol):
    def get_blocking_actors(self, other: CoordinateHolderProtocol) -> Self: ...
    def get_overlapping_actors(self, other: CoordinateHolderProtocol) -> Self: ...
