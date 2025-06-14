from dataclasses import dataclass, field
from app.objects.coordinate_holders_collection import CoordinateHoldersCollection
from app.objects.static_objects_collection import StaticObjectsCollection


@dataclass
class Level:
    coordinate_holders: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)
    static_objects: StaticObjectsCollection = field(default_factory=StaticObjectsCollection)
    grid_width: int = 0
    grid_height: int = 0
