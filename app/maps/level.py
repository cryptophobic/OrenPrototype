from dataclasses import dataclass, field

from app.collections.actor_collection import ActorCollection
from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.collections.static_object_collection import StaticObjectCollection
from app.protocols.engine.grid.grid_protocol import GridProtocol


@dataclass
class Level:
    coordinate_holders: CoordinateHolderCollection = field(default_factory=CoordinateHolderCollection)
    static_objects: StaticObjectCollection = field(default_factory=StaticObjectCollection)
    actors_collection: ActorCollection = field(default_factory=ActorCollection)
    grid: GridProtocol = None
    grid_width: int = 0
    grid_height: int = 0
