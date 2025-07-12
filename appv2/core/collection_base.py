from typing import TypeVar, Generic, Callable, ValuesView, ItemsView, KeysView, Self, Iterator

K = TypeVar("K")  # Key type — e.g. Behaviours, str, int
V = TypeVar("V")  # Value type — e.g. Actor, Behaviour, etc.

class CollectionBase(Generic[K, V]):
    def __init__(self, items: dict[K, V] | None = None):
        self.items: dict[K, V] = items or {}

    def __iter__(self):
        return iter(self.items.values())

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, key: K) -> bool:
        return key in self.items

    def get(self, key: K) -> V | None:
        return self.items.get(key)

    def raw_items(self) -> dict[K, V]:
        return self.items

    def subtract(self, other: Self) -> Self:
        if not other:
            return self
        return type(self)({k: v for k, v in self.items.items() if k not in other})

    def filter(self, predicate: Callable[[V], bool]) -> Self:
        return type(self)({k: v for k, v in self.items.items() if predicate(v)})
