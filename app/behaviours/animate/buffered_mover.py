from app.behaviours.behaviour import register_message_handler, Behaviour
from app.behaviours.types import BufferedMoverState
from app.config import Behaviours
from app.core.vectors import CustomVec2f
from app.engine.message_broker.types import MessageTypes, AnimatePayload
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.BUFFERED_MOVE,
    {
        CoordinateHolder: "on_buffered_move",
    }
)

class BufferedMover(Behaviour):
    name = Behaviours.BUFFERED_MOVER
    supported_receivers = (CoordinateHolder,)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def on_buffered_move(cls, coordinate_holder: CoordinateHolderProtocol, payload: AnimatePayload) -> bool:
        movement_utils = cls.get_movement_utils()
        state = coordinate_holder.behaviour_state.get(cls.name)
        force = 1 if not isinstance(coordinate_holder, UnitProtocol) else coordinate_holder.stats.STR

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState(CustomVec2f.zero())

        state, direction = movement_utils.calculate_buffered_move(coordinate_holder, state, payload.delta_time)

        coordinate_holder.behaviour_state[cls.name] = state
        return movement_utils.try_move(coordinate_holder, direction, force) if direction.is_not_zero() else True
