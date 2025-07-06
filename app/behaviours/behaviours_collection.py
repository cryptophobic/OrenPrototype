from typing import Self, TYPE_CHECKING

from ..bus.message_broker.types import MessageTypes
from ..config import Behaviours
from ..helpers.collection_base import CollectionBase

if TYPE_CHECKING:
    from .behaviour import Behaviour


class BehavioursCollection(CollectionBase[Behaviours, type['Behaviour']]):
    def __init__(self, items: dict[Behaviours, type['Behaviour']] | None = None):
        super().__init__(items or {})

    def can_response_to(self, message_type: MessageTypes) -> Self:
        return type(self)(self.filter(lambda a: a.can_response_to(message_type)))
