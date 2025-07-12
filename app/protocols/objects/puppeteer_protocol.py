from typing import Protocol

from app.engine.message_broker.types import Controls
from app.protocols.objects.actor_protocol import ActorProtocol


class PuppeteerProtocol(ActorProtocol, Protocol):
    puppet: ActorProtocol
    controls: Controls
