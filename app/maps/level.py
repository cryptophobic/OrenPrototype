from dataclasses import dataclass, field

from app.collections.actors_collection import ActorsCollection
from app.collections.coordinate_holders_collection import CoordinateHoldersCollection
from app.collections.static_objects_collection import StaticObjectsCollection
from app.protocols.engine.grid.grid_protocol import GridProtocol


@dataclass
class Level:
    coordinate_holders: CoordinateHoldersCollection = field(default_factory=CoordinateHoldersCollection)
    static_objects: StaticObjectsCollection = field(default_factory=StaticObjectsCollection)
    actors_collection: ActorsCollection = field(default_factory=ActorsCollection)
    grid: GridProtocol = None
    grid_width: int = 0
    grid_height: int = 0
