from dataclasses import dataclass, field
from typing import List

from app.objects.coordinate_holder import CoordinateHolder
from app.objects.static_object import StaticObject

@dataclass
class Level:
    coordinate_holders: List[CoordinateHolder] = field(default_factory=list)
    static_objects: List[StaticObject] = field(default_factory=list)
    grid_width = 0
    grid_height = 0
