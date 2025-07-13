from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.objects.actor import Actor
from app.objects.puppeteer import Puppeteer
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol


class Orchestrator(Actor, OrchestratorProtocol):
    def __init__(self, actors_collection: ActorCollectionProtocol[ActorProtocol], name: str = None):
        super().__init__(name)
        self.moveable_actors = actors_collection.get_behave_as_this(Behaviours.MOVEABLE)
        self.actors_collection: ActorCollectionProtocol = actors_collection

    def get_puppeteers(self) -> PuppeteerCollectionProtocol:
        # TODO: replace with protocols later
        return self.actors_collection.get_by_type(Puppeteer, PuppeteerCollection)
