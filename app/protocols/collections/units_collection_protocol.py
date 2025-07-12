from typing import Protocol, TypeVar, runtime_checkable
from app.protocols.collections.coordinate_holders_collection_protocol import CoordinateHoldersCollectionProtocol
from app.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

@runtime_checkable
class UnitsCollectionProtocol(CoordinateHoldersCollectionProtocol[V], Protocol):
    pass  # Inherits everything needed
