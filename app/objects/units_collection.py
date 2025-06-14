from .actor.unit import Unit
from .coordinate_holders_collection import CoordinateHoldersCollection


class UnitsCollection(CoordinateHoldersCollection[Unit]):
    def __init__(self, items: dict[str, Unit] | None = None):
        super().__init__(items or {})
