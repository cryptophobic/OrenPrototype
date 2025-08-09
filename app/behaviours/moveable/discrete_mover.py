from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, PushedByPayload, IntentionToPlacePayload, MovePayload
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.PUSHED_BY,
    {
        UnitProtocol: "pushed_by_as_unit",
        CoordinateHolderProtocol: "pushed_by_as_coordinate_holder",
    }
)

@register_message_handler(
    MessageTypes.INTENTION_TO_MOVE_DISCRETE,
    {
        CoordinateHolderProtocol: "intention_to_move_discrete",
    }
)

class DiscreteMover(Behaviour):
    name = Behaviours.DISCRETE_MOVER
    supported_receivers = (CoordinateHolderProtocol, UnitProtocol)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def pushed_by_as_unit(cls, unit: UnitProtocol, payload: PushedByPayload) -> bool:
        return cls.pushed_by_as_coordinate_holder(unit, payload)

    @classmethod
    def pushed_by_as_coordinate_holder(cls, coordinate_holder: CoordinateHolderProtocol, payload: PushedByPayload) -> bool:
        if payload.force > 0:
            return cls.get_movement_utils().try_move(coordinate_holder, payload.direction, payload.force - 1)
        else:
            return True

    @classmethod
    def intention_to_move_discrete(cls, coordinate_holder: CoordinateHolderProtocol, payload: MovePayload) -> bool:
        return cls.get_movement_utils().try_move(coordinate_holder, payload.direction, 0)

