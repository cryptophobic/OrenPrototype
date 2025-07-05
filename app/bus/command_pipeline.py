from collections import deque
from dataclasses import dataclass
from typing import Iterator

from ..helpers.staged_queue import StagedQueue
from ..objects.actor.actor import Actor
from ..behaviors.behaviour import BehaviourFn, BehaviourAction


@dataclass
class ActorAction:
    actor: Actor
    behaviour_action: BehaviourAction
    attempts_number: int = 0
    resolved: bool = False

    def resolve(self) -> bool:
        if self.resolved:
            return True
        self.attempts_number += 1
        behaviour = self.actor.__behaviours.get(self.behaviour_action.behaviour)
        if not behaviour:
            return False
        method: BehaviourFn = getattr(behaviour, self.behaviour_action.method_name, None)
        if not callable(method):
            return False

        result = method(*self.behaviour_action.args, **self.behaviour_action.kwargs)
        self.resolved = result is True
        return self.resolved

def wrap_action(actor: Actor, behaviour_action: BehaviourAction) -> ActorAction:
    return ActorAction(actor, behaviour_action)

def wrap_actions(actor: Actor, behaviour_actions: deque[BehaviourAction]) -> Iterator[ActorAction]:
    for action in behaviour_actions:
        yield wrap_action(actor, action)

class CommandPipeline:
    MAX_RECURSION_DEPTH = 5

    def __init__(self):
        self._queue: StagedQueue[ActorAction] = StagedQueue[ActorAction]()

    def post(self, action: ActorAction):
        self._queue.append_first(action)

    def process_actions(self):
        return self.process_queue(self._queue)

    def __flush_pending(self, actor: Actor, state_changed, depth):
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
