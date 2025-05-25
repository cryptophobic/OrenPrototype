from collections import deque
from typing import Callable

from ui.actors.actor import Actor


class EventBus:
    def __init__(self):
        self._queue: deque[tuple[Actor, Callable[[], None]]] = deque()

    def post(self, actor: Actor, callback: Callable):
        self._queue.append((actor, callback))

    def conflict(self, actor: Actor, resolver: Callable):
        self._queue.appendleft((actor, resolver))

    def flush(self) -> int:
        last_actor: Actor | None = None
        processed = 0
        while self._queue:
            actor, event = self._queue.popleft()
            if last_actor and actor.name != last_actor.name:
                last_actor.actions.commit()
            event()
            last_actor = actor

        if last_actor:
            processed += last_actor.actions.commit()

        return processed
