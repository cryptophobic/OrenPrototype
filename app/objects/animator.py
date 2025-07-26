from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.objects.actor import Actor
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.coordinate_holder_collection_protocol import CoordinateHolderCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.animator_protocol import AnimatorProtocol


class Animator(Actor, AnimatorProtocol):
    def __init__(self, actor_collection: ActorCollectionProtocol[ActorProtocol], name: str = None):
        super().__init__(name)
        self.actor_collection: ActorCollectionProtocol = actor_collection
        self.coordinate_holders: CoordinateHolderCollectionProtocol = actor_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection)
