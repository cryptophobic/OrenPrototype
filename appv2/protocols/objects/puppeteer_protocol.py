from typing import Protocol

from actor_protocol import ActorProtocol
from appv2.engine.message_broker.types import Controls


class PuppeteerProtocol(ActorProtocol, Protocol):
    puppet: ActorProtocol
    controls: Controls
