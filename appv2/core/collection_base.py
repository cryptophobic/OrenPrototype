from typing import TypeVar, Generic, Callable, ValuesView, ItemsView, KeysView
from collections import UserDict

K = TypeVar("K")  # Key type — e.g. Behaviours, str, int
V = TypeVar("V")  # Value type — e.g. Actor, Behaviour, etc.

class CollectionBase(Generic[K, V], UserDict[K, V]):
    def __init__(self, items: dict[K, V] | None = None):
        super().__init__(items or {})

    def values(self) -> ValuesView[V]:
        return super().values()

    def keys(self) -> KeysView[K]:
        return super().keys()

    def items(self) -> ItemsView[K, V]:
        return super().items()

    def filter(self, predicate: Callable[[V], bool]) -> dict[K, V]:
        return {k: v for k, v in self.data.items() if predicate(v)}
