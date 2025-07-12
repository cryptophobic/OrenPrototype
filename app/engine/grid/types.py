from dataclasses import dataclass, field

from app.collections.coordinate_holders_collection import CoordinateHoldersCollection


@dataclass
class PlaceToPositionResult:
    placed: bool = False
    blocked: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)
    overlapped: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)
