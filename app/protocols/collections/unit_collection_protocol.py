from typing import Protocol, TypeVar, runtime_checkable
from app.protocols.collections.coordinate_holder_collection_protocol import CoordinateHolderCollectionProtocol
from app.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

@runtime_checkable
class UnitCollectionProtocol(CoordinateHolderCollectionProtocol[V], Protocol):
    pass  # Inherits everything needed
