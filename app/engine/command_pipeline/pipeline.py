from collections import deque
from dataclasses import dataclass
from typing import Iterator, Callable, Optional, Iterable

from app.behaviours.types import BehaviourAction
from app.core.staged_queue import StagedQueue
from app.engine.message_broker.types import Payload
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
        method: Callable[[ActorProtocol, Payload], bool] = getattr(behaviour, self.behaviour_action.method_name, None)
        # TODO: Debug why method_names are incorrect
        if not callable(method):
            return False

        self.resolved = method(self.actor, self.behaviour_action.payload)
        return self.resolved

class CommandPipeline:
    MAX_RECURSION_DEPTH = 5

    @classmethod
    def wrap_action(cls, actor: ActorProtocol, behaviour_action: BehaviourAction) -> ActorAction:
        return ActorAction(actor, behaviour_action)

    @classmethod
    def wrap_actions(cls, actor: ActorProtocol, behaviour_actions: deque[BehaviourAction]) -> Iterator[ActorAction]:
        for action in behaviour_actions:
            yield cls.wrap_action(actor, action)

    @classmethod
    def drained_wrapped_actions(cls, initiators: Iterable[ActorProtocol]) -> Iterator[ActorAction]:
        for initiator in initiators:
            pending_actions = initiator.pending_actions
            # setting to new deque() because it is important to keep untouched
            # the one that passed as a parameter to wrap_actions
            initiator.pending_actions = deque()
            yield from cls.wrap_actions(initiator, pending_actions)

    def __init__(self):
        self.actor_collection: Optional[ActorCollectionProtocol[ActorProtocol]] = None
        self._queue: StagedQueue[ActorAction] = StagedQueue[ActorAction]()

    def process(self, initiators: Iterable[ActorProtocol]) -> bool:
        queue = StagedQueue[ActorAction]()
        queue.middle = self.drained_wrapped_actions(initiators)
        state_changed = self.process_queue(queue)

        return state_changed

    def __flush_pending(self, state_changed, depth) -> bool:
        queue = StagedQueue[ActorAction]()
        queue.middle = self.drained_wrapped_actions(self.actor_collection.get_pending_actors())
        state_changed = self.process_queue(
            queue=queue,
            state_changed=state_changed,
            depth=depth + 1)

        return state_changed

    def __flush_pending_actor(self, actor: ActorProtocol, state_changed, depth):
        if actor.pending_actions:
            queue = StagedQueue[ActorAction]()
            queue.middle = self.drained_wrapped_actions([actor])

            state_changed = self.process_queue(
                queue=queue,
                state_changed=state_changed,
                depth=depth + 1)

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
            state_changed = self.__flush_pending_actor(actor, state_changed, depth)
            resolved = action.resolve()

            state_changed = resolved or state_changed
            if not resolved:
                queue.append_left_first(action) if actor.pending_actions else queue.append_last(action)

            state_changed = self.__flush_pending(state_changed, depth)

        return state_changed

    def clear(self):
        self._queue = StagedQueue[ActorAction]()
