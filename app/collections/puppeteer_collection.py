from typing import TypeVar

from app.collections.actor_collection import ActorCollection
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.unit_protocol import UnitProtocol

V = TypeVar("V", bound=UnitProtocol)

class PuppeteerCollection(ActorCollection[V], PuppeteerCollectionProtocol[V]):
    pass