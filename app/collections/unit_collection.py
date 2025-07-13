from typing import TypeVar

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.protocols.collections.unit_collection_protocol import UnitCollectionProtocol
from app.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

class UnitCollection(CoordinateHolderCollection[V], UnitCollectionProtocol[V]):
    pass