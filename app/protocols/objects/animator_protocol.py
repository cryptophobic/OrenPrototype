from typing import Protocol, runtime_checkable

from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.coordinate_holder_collection_protocol import CoordinateHolderCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol


@runtime_checkable
class AnimatorProtocol(ActorProtocol, Protocol):
    """Protocol for animators that manage collections of actors."""
    
    actor_collection: ActorCollectionProtocol[ActorProtocol]
    coordinate_holders: CoordinateHolderCollectionProtocol