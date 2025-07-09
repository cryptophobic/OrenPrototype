from typing import TypeVar, Self

from appv2.collections.coordinate_holders_collection import CoordinateHoldersCollection
from appv2.protocols.objects.static_object_protocol import StaticObjectProtocol

T = TypeVar("T", bound=StaticObjectProtocol)

class StaticObjectsCollection(CoordinateHoldersCollection[T]):
    def __init__(self, items: dict[str, T] | None = None):
        super().__init__(items or {})

    def get_taller_than(self, height, inclusive = False) -> Self:
        return type(self)(self.filter(lambda a: a.height >= height if inclusive else a.height > height))

    def get_shorter_than(self, height, inclusive = False) -> Self:
        return type(self)(self.filter(lambda a: a.height <= height if inclusive else a.height < height))

    def get_with_height(self, height) -> Self:
        return type(self)(self.filter(lambda a: a.height == height))
