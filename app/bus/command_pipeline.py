from collections import deque
from dataclasses import dataclass, field

from app.config import Behaviours
from app.objects.actor.actor import Actor


@dataclass
class ActorAction:
    actor: Actor
    behaviour: Behaviours
    method_name: str
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    attempts_number: int = 0

    def resolve(self) -> bool:
        self.attempts_number += 1
        behaviour = self.actor.__behaviours.get(self.behaviour)
        if not behaviour:
            return False
        method = getattr(behaviour, self.method_name, None)
        if not callable(method):
            return False
        return method(*self.args, **self.kwargs)


class CommandPipeline:
    MAX_RECURSION_DEPTH = 5

    def __init__(self):
        self._queue: deque[ActorAction] = deque()

    def post(self, action: ActorAction):
        self._queue.append(action)

    def process_actions(self,
                        queue: deque[ActorAction] = None,
                        state_changed: bool = False,
                        depth: int = 0):
        queue = queue or self._queue
        if depth >= CommandPipeline.MAX_RECURSION_DEPTH:
            return state_changed

        while queue:
            action = queue.popleft()
            if action.attempts_number >= 2:
                continue

            actor = action.actor
            if actor.blocking_actions:
                state_changed = self.process_actions(actor.blocking_actions, state_changed=state_changed, depth=depth + 1) or state_changed

            resolved = action.resolve()
            state_changed = resolved or state_changed
            if not resolved and actor.blocking_actions:
                queue.appendleft(action)

        return state_changed

    def clear(self):
        self._queue.clear()
