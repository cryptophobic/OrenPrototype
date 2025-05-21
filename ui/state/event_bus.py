from collections import deque
from typing import Callable

class EventBus:
    def __init__(self):
        self._queue: deque[Callable] = deque()

    def post(self, callback: Callable):
        self._queue.append(callback)

    def dispatch(self):
        while self._queue:
            event = self._queue.popleft()
            event()
