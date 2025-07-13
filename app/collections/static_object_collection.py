from typing import TypeVar, Self

from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.protocols.collections.static_object_collection_protocol import StaticObjectCollectionProtocol
from app.protocols.objects.static_object_protocol import StaticObjectProtocol

T = TypeVar("T", bound=StaticObjectProtocol)

class StaticObjectCollection(CoordinateHolderCollection[T], StaticObjectCollectionProtocol[T]):
    def get_taller_than(self, height, inclusive = False) -> Self:
        return self.filter(lambda a: a.height >= height if inclusive else a.height > height)

    def get_shorter_than(self, height, inclusive = False) -> Self:
        return self.filter(lambda a: a.height <= height if inclusive else a.height < height)

    def get_with_height(self, height) -> Self:
        return self.filter(lambda a: a.height == height)
