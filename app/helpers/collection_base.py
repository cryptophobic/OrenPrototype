from typing import TypeVar, Generic, Iterator, Callable, ValuesView, ItemsView, KeysView
from collections import UserDict

T = TypeVar("T")

class CollectionBase(Generic[T], UserDict[str, T]):
    def __init__(self, items: dict[str, T] | None = None):
        super().__init__(items or {})

    def values(self) -> ValuesView[T]:
        return super().values()

    def keys(self) -> KeysView[str]:
        return super().keys()

    def items(self) -> ItemsView[str, T]:
        return super().items()

    def filter(self, predicate: Callable[[T], bool]) -> dict[str, T]:
        return {k: v for k, v in self.data.items() if predicate(v)}
