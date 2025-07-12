from collections import deque
from typing import Deque, Iterator, Optional, TypeVar, Generic

T = TypeVar("T")


class StagedQueue(Generic[T]):
    def __init__(
        self,
        first: Optional[Deque[T]] = None,
        middle: Optional[Iterator[T]] = None,
        last: Optional[Deque[T]] = None,
    ):
        self.first = first or deque()
        self.middle = middle or iter(())
        self.last = last or deque()

    def __iter__(self) -> Iterator[T]:
        while True:
            if self.first:
                yield self.first.popleft()
            else:
                try:
                    yield next(self.middle)
                except StopIteration:
                    if self.last:
                        yield self.last.popleft()
                    else:
                        break

    def append(self, item: T):
        self.append_first(item)

    def append_first(self, item: T):
        self.first.append(item)

    def append_left_first(self, item: T):
        self.first.appendleft(item)

    def extend_left_first(self, items: deque[T]):
        self.first.extendleft(items)

    def append_last(self, item: T):
        self.last.append(item)

    def append_left_last(self, item: T):
        self.last.appendleft(item)

    def to_list(self) -> list[T]:
        return list(self.first) + list(self.middle) + list(self.last)

