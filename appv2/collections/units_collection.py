from typing import TypeVar

from appv2.collections.coordinate_holders_collection import CoordinateHoldersCollection
from appv2.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

class UnitsCollection(CoordinateHoldersCollection[V]):
    pass