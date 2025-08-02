from app.behaviours.behaviour import register_message_handler, Behaviour
from app.behaviours.types import BufferedMoverState
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, AnimatePayload, SetVelocityPayload, StopPayload
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.BUFFERED_MOVE,
    {
        CoordinateHolder: "on_buffered_move",
    }
)

@register_message_handler(
    MessageTypes.INTENTION_TO_MOVE,
    {
        CoordinateHolder: "intention_to_move",
    }
)

@register_message_handler(
    MessageTypes.INTENTION_TO_STOP,
    {
        CoordinateHolder: "intention_to_stop",
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
            state = BufferedMoverState()

        state, direction = movement_utils.calculate_buffered_move(coordinate_holder, state, payload.delta_time)

        if direction.x != 0 and state.clear_velocity.x:
            coordinate_holder.intent_velocity.x = 0

        if direction.y != 0 and state.clear_velocity.y:
            coordinate_holder.intent_velocity.y = 0

        coordinate_holder.behaviour_state[cls.name] = state
        return movement_utils.try_move(coordinate_holder, direction, force) if direction.is_not_zero() else True

    @classmethod
    def intention_to_move(cls, coordinate_holder: CoordinateHolderProtocol, payload: SetVelocityPayload) -> bool:
        intent_velocity = payload.velocity.normalized()
        if isinstance(coordinate_holder, UnitProtocol):
            intent_velocity *= coordinate_holder.stats.speed

        coordinate_holder.intent_velocity = intent_velocity
        state = coordinate_holder.behaviour_state.get(cls.name)

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState()

        if payload.velocity.x != 0:
            state.clear_velocity.x = 0

        if payload.velocity.y != 0:
            state.clear_velocity.y = 0

        coordinate_holder.behaviour_state[cls.name] = state

        return True

    @classmethod
    def intention_to_stop(cls, coordinate_holder: CoordinateHolderProtocol, payload: StopPayload) -> bool:
        state = coordinate_holder.behaviour_state.get(cls.name)

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState()

        state.clear_velocity.x |= payload.direction.x
        state.clear_velocity.y |= payload.direction.y

        coordinate_holder.behaviour_state[cls.name] = state

        return True
