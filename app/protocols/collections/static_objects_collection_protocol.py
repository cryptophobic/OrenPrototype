from typing import Protocol, Self, TypeVar, runtime_checkable
from app.protocols.collections.coordinate_holders_collection_protocol import CoordinateHoldersCollectionProtocol
from app.protocols.objects.static_object_protocol import StaticObjectProtocol

V = TypeVar("V", bound=StaticObjectProtocol)

@runtime_checkable
class StaticObjectsCollectionProtocol(CoordinateHoldersCollectionProtocol[V], Protocol):
    def get_taller_than(self, height: float, inclusive: bool = False) -> Self: ...
    def get_shorter_than(self, height: float, inclusive: bool = False) -> Self: ...
    def get_with_height(self, height: float) -> Self: ...
