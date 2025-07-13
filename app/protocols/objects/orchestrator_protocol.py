from typing import runtime_checkable

from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


@runtime_checkable
class OrchestratorProtocol(ActorProtocol):
    actors_collection: ActorCollectionProtocol