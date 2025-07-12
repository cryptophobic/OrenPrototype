from typing import TypeVar

from app.collections.coordinate_holders_collection import CoordinateHoldersCollection
from app.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

class UnitsCollection(CoordinateHoldersCollection[V]):
    pass