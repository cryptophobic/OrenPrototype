from collections import deque
from dataclasses import dataclass
from typing import Iterator, Callable, Optional

from app.behaviours.types import BehaviourAction
from app.core.staged_queue import StagedQueue
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


@dataclass
class ActorAction:
    actor: ActorProtocol
    behaviour_action: BehaviourAction
    attempts_number: int = 0
    resolved: bool = False

    def resolve(self) -> bool:
        if self.resolved:
            return True
        self.attempts_number += 1
        behaviour = self.actor.behaviours.get(self.behaviour_action.behaviour)
        if not behaviour:
            return False
        method: Callable[[...], bool] = getattr(behaviour, self.behaviour_action.method_name, None)
        if not callable(method):
            return False

        self.resolved = method(*self.behaviour_action.args, **self.behaviour_action.kwargs)
        return self.resolved

def wrap_action(actor: ActorProtocol, behaviour_action: BehaviourAction) -> ActorAction:
    return ActorAction(actor, behaviour_action)

def wrap_actions(actor: ActorProtocol, behaviour_actions: deque[BehaviourAction]) -> Iterator[ActorAction]:
    for action in behaviour_actions:
        yield wrap_action(actor, action)

class CommandPipeline:
    MAX_RECURSION_DEPTH = 5

    def __init__(self):
        self.actor_collection: Optional[ActorCollectionProtocol[ActorProtocol]] = None
        self._queue: StagedQueue[ActorAction] = StagedQueue[ActorAction]()

    '''Runs every frame, clears all possible leftovers from previous frame'''
    def flush_pending_actions(self) -> deque:
        queue: deque[ActorAction] = deque()
        if self.actor_collection:
            for actor in self.actor_collection.get_pending_actors():
                queue.extend(wrap_actions(actor, actor.pending_actions))
                actor.pending_actions.clear()

        return queue

    def process(self, orchestrator: ActorProtocol) -> bool:
        leftovers = self.flush_pending_actions()
        queue = StagedQueue[ActorAction](
            first=leftovers,
            middle=wrap_actions(orchestrator, orchestrator.pending_actions),
            last=None,
        )
        orchestrator.pending_actions.clear()
        return self.process_queue(queue)

    def __flush_pending(self, actor: ActorProtocol, state_changed, depth):
        if actor.pending_actions:
            state_changed = self.process_queue(
                queue=StagedQueue[ActorAction](
                    first=None,
                    middle=wrap_actions(actor, actor.pending_actions),
                    last=None,
                ),
                state_changed=state_changed,
                depth=depth + 1)

            actor.pending_actions.clear()

        return state_changed

    def process_queue(self,
                        queue: StagedQueue[ActorAction] = StagedQueue[ActorAction](),
                        state_changed: bool = False,
                        depth: int = 0):

        if depth >= CommandPipeline.MAX_RECURSION_DEPTH:
            return state_changed

        for action in queue:
            if action.attempts_number >= 2:
                continue

            actor = action.actor
            state_changed = self.__flush_pending(actor, state_changed, depth)
            resolved = action.resolve()
            state_changed = resolved or state_changed
            if not resolved:
                queue.append_left_first(action) if actor.pending_actions else queue.append_last(action)
            elif actor.pending_actions:
                state_changed = self.__flush_pending(actor, state_changed, depth)

        return state_changed

    def clear(self):
        self._queue = StagedQueue[ActorAction]()
