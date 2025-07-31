from typing import runtime_checkable, Protocol

from app.core.types import KeyPressEventLogRecords
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol

@runtime_checkable
class OrchestratorProtocol(ActorProtocol, Protocol):
    delta_time: float
    actors_collection: ActorCollectionProtocol
    moveable_actors: ActorCollectionProtocol
    puppeteer: PuppeteerProtocol
    messenger: MessageBrokerProtocol

    def get_puppeteers(self) -> PuppeteerCollectionProtocol: ...
    def set_puppet(self, name: str) -> None: ...
    def process_input(self, keys_down: list[int], key_press_input: KeyPressEventLogRecords) -> None: ...
    def process_tick(self, delta_time: float) -> None: ...