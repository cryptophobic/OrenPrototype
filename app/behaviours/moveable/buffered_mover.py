from app.behaviours.behaviour import Behaviour, register_message_handler
from app.behaviours.types import BufferedMoverState
from app.config import Behaviours
from app.core.event_bus.events import Events, AnimationUpdatePayload
from app.engine.message_broker.types import MessageTypes, AnimatePayload, StopPayload, MovePayload
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol

class BufferedMover(Behaviour):
    name = Behaviours.BUFFERED_MOVER
    supported_receivers = (CoordinateHolderProtocol,)

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    @register_message_handler (MessageTypes.BUFFERED_MOVE, for_=(CoordinateHolderProtocol,))
    def on_buffered_move(cls, coordinate_holder: CoordinateHolderProtocol, payload: AnimatePayload) -> bool:
        movement_utils = cls.get_movement_utils()
        state = coordinate_holder.behaviour_state.get(cls.name)
        force = 1 if not isinstance(coordinate_holder, UnitProtocol) else coordinate_holder.stats.STR

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState()

        state, moving_direction = movement_utils.calculate_buffered_move(coordinate_holder, state, payload.delta_time)
        if moving_direction.is_not_zero():
            state.intent_velocity_normalised = state.intent_velocity.normalized()
            if isinstance(coordinate_holder, UnitProtocol):
                state.intent_velocity_normalised *= coordinate_holder.stats.speed

        if isinstance(coordinate_holder, UnitProtocol):
            animation, direction = movement_utils.get_animation_and_textures(state.intent_velocity_normalised, coordinate_holder)
            need_to_update = (coordinate_holder.shape.current_animation != animation
                or coordinate_holder.shape.direction != direction)
            if need_to_update:
                coordinate_holder.shape.current_animation = animation
                coordinate_holder.shape.direction = direction

                event_bus = cls.get_event_bus()
                event_bus.publish(Events.AnimationUpdate, AnimationUpdatePayload(coordinate_holder.name))


        coordinate_holder.behaviour_state[cls.name] = state
        return movement_utils.try_move(coordinate_holder, moving_direction, force) if moving_direction.is_not_zero() else True

    @classmethod
    @register_message_handler (MessageTypes.INTENTION_TO_MOVE, for_=(CoordinateHolderProtocol,))
    def intention_to_move(cls, coordinate_holder: CoordinateHolderProtocol, payload: MovePayload) -> bool:
        state = coordinate_holder.behaviour_state.get(cls.name)

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState()

        if payload.direction.x != 0:
            state.intent_velocity.x = payload.direction.x
            state.clear_velocity.x = 0

        if payload.direction.y != 0:
            state.intent_velocity.y = payload.direction.y
            state.clear_velocity.y = 0

        state.intent_velocity_normalised = state.intent_velocity.normalized()
        if isinstance(coordinate_holder, UnitProtocol):
            state.intent_velocity_normalised *= coordinate_holder.stats.speed

        coordinate_holder.behaviour_state[cls.name] = state

        return True

    @classmethod
    @register_message_handler (MessageTypes.INTENTION_TO_STOP, for_=(CoordinateHolderProtocol,))
    def intention_to_stop(cls, coordinate_holder: CoordinateHolderProtocol, payload: StopPayload) -> bool:
        state = coordinate_holder.behaviour_state.get(cls.name)

        if not isinstance(state, BufferedMoverState):
            state = BufferedMoverState()

        state.clear_velocity.x |= payload.direction.x
        state.clear_velocity.y |= payload.direction.y

        coordinate_holder.behaviour_state[cls.name] = state

        return True
