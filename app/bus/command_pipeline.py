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
        return method(*self.args, **self.kwargs) == True


class CommandPipeline:
    def __init__(self):
        self._queue: deque[ActorAction] = deque()

    def post(self, action: ActorAction):
        self._queue.append(action)

    def process_queue(self, queue: deque[ActorAction]):
        while queue:
            action = queue.popleft()
            if action.attempts_number >= 2:
                continue

            actor = action.actor
            if actor.blocking_actions:
                self.process_queue(actor.blocking_actions)

            resolved = action.resolve()
            if not resolved and actor.blocking_actions:
                queue.appendleft(action)

    def process_actions(self) -> bool:
        state_changed = True

        self.process_queue(self._queue)

        return state_changed
