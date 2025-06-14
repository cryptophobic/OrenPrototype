from .actor.actor import Actor
from .actor.static_object import StaticObject
from .coordinate_holders_collection import CoordinateHoldersCollection


class StaticObjectsCollection(CoordinateHoldersCollection[StaticObject]):
    def __init__(self, items: dict[str, StaticObject] | None = None):
        super().__init__(items or {})

    def get_taller_than(self, height, inclusive = False) -> 'StaticObjectsCollection':
        return StaticObjectsCollection(self.filter(lambda a: a.height >= height if inclusive else a.height > height))

    def get_shorter_than(self, height, inclusive = False) -> 'StaticObjectsCollection':
        return StaticObjectsCollection(self.filter(lambda a: a.height <= height if inclusive else a.height < height))

    def get_with_height(self, height) -> 'StaticObjectsCollection':
        return StaticObjectsCollection(self.filter(lambda a: a.height == height))
