from app.behaviours.behaviour import Behaviour, handles
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, IntentionToPlacePayload
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class Cursor(Behaviour):
    name = Behaviours.CURSOR
    supported_receivers = (CoordinateHolderProtocol,)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    @handles(MessageTypes.INTENTION_TO_PLACE, for_=(CoordinateHolderProtocol,))
    def intention_to_place(cls, coordinate_holder: CoordinateHolderProtocol, payload: IntentionToPlacePayload) -> bool:
        return cls.get_movement_utils().try_place(coordinate_holder, payload.to_place)

