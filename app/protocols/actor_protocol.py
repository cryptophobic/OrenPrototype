from abc import ABC, abstractmethod
from collections import deque
from typing import Protocol, List, runtime_checkable

from ..behaviours.types import BehaviourAction
from ..bus.message_broker.types import MessageBody
from ..config import Behaviours


@runtime_checkable
class ActorProtocol(Protocol):
    """Protocol defining the interface that actors must implement for behaviours to work with them."""
    
    active: bool
    pending_actions: deque[BehaviourAction]
    
    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]:
        """Handle incoming messages and return response actions."""
        ...
    
    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        """Check if actor has a specific behaviour."""
        ...
    
    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        """Check if actor has all specified behaviours."""
        ...


@runtime_checkable
class BehaviourProtocol(Protocol):
    """Protocol defining the interface that behaviours must implement."""
    
    name: Behaviours
    
    @classmethod
    def on_message(cls, receiver: ActorProtocol, message_body: MessageBody) -> deque[BehaviourAction]:
        """Handle a message for a specific receiver."""
        ...
    
    @classmethod
    def can_handle(cls, receiver: ActorProtocol, message_type) -> bool:
        """Check if this behaviour can handle a message type for a receiver."""
        ...


class ActorInterface(ABC):
    """Abstract base class for actors that need to be extended with specific implementations."""
    
    @abstractmethod
    def on_message(self, message_body: MessageBody) -> deque[BehaviourAction]:
        pass
    
    @abstractmethod
    def is_behave_as_this(self, behaviour: Behaviours) -> bool:
        pass
    
    @abstractmethod
    def is_behave_as_them(self, behaviours: List[Behaviours]) -> bool:
        pass