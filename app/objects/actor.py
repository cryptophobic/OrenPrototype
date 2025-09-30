from collections import deque
from typing import List, Optional

from app.behaviours.behaviour_states_store import BehaviourStateStore
from app.collections.behaviour_collection import BehaviourCollection
from app.core.event_bus.bus import bus
from app.core.event_bus.events import Events
import app.core.event_bus.types as event_types
from app.engine.message_broker.types import MessageBody
from app.config import Behaviours
from app.behaviours.types import BehaviourAction, BufferedMoverState
from app.protocols.collections.behaviour_collection_protocol import BehaviourCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


class Actor(ActorProtocol):
    def __init__(self, name: str = None, is_active = False):
        self.event_bus = bus
        self.name: str = name
        self.behaviour_state: BehaviourStateStore = BehaviourStateStore()
        self.is_active: bool = False
        self.is_deleted: bool = False
        self.pending_actions: deque[BehaviourAction] = deque()
        self.behaviours: BehaviourCollectionProtocol = BehaviourCollection()
        if is_active:
            self.activate()

    @property
    def id(self) -> str:
        return self.name

    def activate(self) -> None:
        self.event_bus.emit(
            Events.RegisterActor,
            event_types.RegisterActorPayload(
                object_name=self.name,
            )
        )
        self.is_active = True

    def deactivate(self) -> None:
        self.event_bus.emit(Events.UnregisterActor, event_types.UnregisterObjectPayload(object_name=self.name))
        self.is_active = False

    def delete(self) -> None:
        self.event_bus.emit(Events.UnregisterActor, event_types.UnregisterObjectPayload(object_name=self.name))
        self.is_deleted = True

    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]:
        filtered_behaviours = self.behaviours.can_respond_to(message_body.message_type)
        response_actions: deque[BehaviourAction] = deque()
        for behaviour in filtered_behaviours:
            response_actions.extend(behaviour.on_message(self, message_body))

        return response_actions

    def extract_behaviour_data(self, behaviour: Behaviours) -> Optional[BufferedMoverState]:
        return self.behaviour_state.get(behaviour)

    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        return self.is_behave_as_them([behaviour])

    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        return all(behaviour in self.behaviours for behaviour in behaviours)

    def is_behave_as_any(self, behaviours: List[Behaviours]) -> bool:
        return any(behaviour in self.behaviours for behaviour in behaviours)

    def add_behaviour(self, behaviour: Behaviours) -> None:
        self.behaviours.set(behaviour)

    def remove_behaviour(self, behaviour: Behaviours) -> None:
        self.behaviours.remove(behaviour)
