from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, SetVelocityPayload
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.INTENTION_TO_MOVE,
    {
        CoordinateHolder: "intention_to_move",
    }
)

class BufferedMover(Behaviour):
    name = Behaviours.BUFFERED_MOVER
    supported_receivers = (CoordinateHolder,)

    @classmethod
    def intention_to_move(cls, unit: UnitProtocol, payload: SetVelocityPayload) -> bool:
        intent_velocity = payload.velocity.normalized() * unit.stats.speed
        unit.intent_velocity = intent_velocity
        return True
