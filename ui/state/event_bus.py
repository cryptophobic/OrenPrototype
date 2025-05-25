from collections import deque
from typing import Callable

from map.battlefield import battlefield
from ui.actors.actor import Actor


class EventBus:
    def __init__(self, conflict_resolver: Callable):
        self.conflict_resolver = conflict_resolver
        self._queue: deque[tuple[Actor, Callable[[], None]]] = deque()

    def post(self, actor: Actor, callback: Callable):
        self._queue.append((actor, callback))

    def conflict(self, actor: Actor, resolver: Callable):
        self._queue.appendleft((actor, resolver))

    def __commit_actor_actions(self, actor: Actor):
        from_cell = actor.coordinates
        result, actor.coordinates = actor.actions.commit(actor.coordinates)
        to_cell = actor.coordinates
        battlefield.move_unit(from_cell, to_cell)
        if not result:
            self.conflict(actor, self.conflict_resolver)

    def flush(self) -> int:
        last_actor: Actor | None = None
        while self._queue:
            actor, event = self._queue.popleft()
            if last_actor and actor.name != last_actor.name:
                self.__commit_actor_actions(last_actor)
            event()
            last_actor = actor

        if last_actor:
            self.__commit_actor_actions(last_actor)

        return 1
