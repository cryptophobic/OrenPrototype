from app.objects.actor import Actor
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


class Orchestrator(Actor):
    def __init__(self, actors_collection: ActorCollectionProtocol[ActorProtocol], name: str = None):
        super().__init__(name)
        self.actors_collection: ActorCollectionProtocol = actors_collection
