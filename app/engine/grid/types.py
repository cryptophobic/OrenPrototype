from dataclasses import dataclass, field

from app.collections.coordinate_holder_collection import CoordinateHolderCollection


@dataclass
class PlaceToPositionResult:
    placed: bool = False
    blocked: CoordinateHolderCollection = field(default_factory=CoordinateHolderCollection)
    overlapped: CoordinateHolderCollection = field(default_factory=CoordinateHolderCollection)
