from typing import runtime_checkable

from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


class OrchestratorProtocol(ActorProtocol):
    actors_collection: ActorCollectionProtocol
    moveable_actors: ActorCollectionProtocol

    def get_puppeteers(self) -> PuppeteerCollectionProtocol: ...
    def set_puppet(self, name: str): ...