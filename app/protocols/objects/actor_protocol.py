from collections import deque
from typing import Protocol, List, runtime_checkable, Self, Optional

from app.behaviours.behaviour_states_store import BehaviourStateStore
from app.engine.message_broker.types import MessageBody
from app.behaviours.types import BehaviourAction, BehaviourStates, BufferedMoverState
from app.config import Behaviours
from app.protocols.collections.behaviour_collection_protocol import BehaviourCollectionProtocol


@runtime_checkable
class ActorProtocol(Protocol):
    name: str
    is_active: bool
    is_deleted: bool
    pending_actions: deque[BehaviourAction]
    behaviours: BehaviourCollectionProtocol
    behaviour_state: BehaviourStateStore

    @property
    def id(self) -> str: ...
    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]: ...
    def is_behave_as_this(self, behaviour: Behaviours) -> bool: ...
    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool: ...
    def is_behave_as_any(self, behaviours: List[Behaviours]) -> bool: ...
    def add_behaviour(self, behaviour: Behaviours) -> None: ...
    def remove_behaviour(self, behaviour: Behaviours) -> None: ...
    def extract_behaviour_data(self, behaviour: Behaviours) -> Optional[BufferedMoverState]: ...
