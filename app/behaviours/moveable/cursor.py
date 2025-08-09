from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, IntentionToPlacePayload
from app.objects.coordinate_holder import CoordinateHolder


@register_message_handler(
    MessageTypes.INTENTION_TO_PLACE,
    {
        CoordinateHolder: "INTENTION_TO_PLACE",
    }
)

class Cursor(Behaviour):
    name = Behaviours.CURSOR
    supported_receivers = (CoordinateHolder,)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def intention_to_place(cls, coordinate_holder: CoordinateHolder, payload: IntentionToPlacePayload) -> bool:
        return cls.get_movement_utils().try_place(coordinate_holder, payload.to_place)

