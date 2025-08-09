from app.behaviours.behaviour import Behaviour, register_message_handler
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, PushedByPayload, MovePayload
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class DiscreteMover(Behaviour):
    name = Behaviours.DISCRETE_MOVER
    supported_receivers = (CoordinateHolderProtocol,)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    @register_message_handler (MessageTypes.PUSHED_BY, for_=(CoordinateHolderProtocol,))
    def pushed_by(cls, coordinate_holder: CoordinateHolderProtocol, payload: PushedByPayload) -> bool:
        print(f"pushed by coordinate holder: {coordinate_holder.name}")
        if payload.force > 0:
            return cls.get_movement_utils().try_move(coordinate_holder, payload.direction, payload.force - 1)
        else:
            return True

    @classmethod
    @register_message_handler (MessageTypes.INTENTION_TO_MOVE_DISCRETE, for_=(CoordinateHolderProtocol,))
    def intention_to_move_discrete(cls, coordinate_holder: CoordinateHolderProtocol, payload: MovePayload) -> bool:
        return cls.get_movement_utils().try_move(coordinate_holder, payload.direction, 0)

