from typing import TypeVar

from .actor.unit import Unit
from .coordinate_holders_collection import CoordinateHoldersCollection

V = TypeVar("V", bound=Unit)

class UnitsCollection(CoordinateHoldersCollection[V]):
    def __init__(self, items: dict[str, Unit] | None = None):
        super().__init__(items or {})
