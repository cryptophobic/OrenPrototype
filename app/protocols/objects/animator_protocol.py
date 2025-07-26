from typing import Protocol

from app.protocols.objects.actor_protocol import ActorProtocol


class AnimatorProtocol(ActorProtocol, Protocol):
    pass