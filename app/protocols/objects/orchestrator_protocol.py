from typing import runtime_checkable, Protocol

from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol

@runtime_checkable
class OrchestratorProtocol(ActorProtocol, Protocol):
    actors_collection: ActorCollectionProtocol
    moveable_actors: ActorCollectionProtocol
    puppeteer: PuppeteerProtocol

    def get_puppeteers(self) -> PuppeteerCollectionProtocol: ...
    def set_puppet(self, name: str): ...