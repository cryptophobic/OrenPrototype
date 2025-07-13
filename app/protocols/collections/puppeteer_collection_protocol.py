from typing import Protocol, TypeVar, runtime_checkable

from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol

V = TypeVar("V", bound=PuppeteerProtocol)

@runtime_checkable
class PuppeteerCollectionProtocol(ActorCollectionProtocol[V], Protocol):
    pass  # Inherits everything needed
