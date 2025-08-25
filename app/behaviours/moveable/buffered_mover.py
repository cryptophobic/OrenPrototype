from app.behaviours.behaviour import Behaviour, register_message_handler
from app.behaviours.types import BufferedMoverState, SimpleVec2Bool
from app.config import Behaviours
from app.core.event_bus.events import Events, AnimationUpdatePayload
from app.core.vectors import CustomVec2f
from app.engine.message_broker.types import MessageTypes, AnimatePayload, StopPayload, MovePayload, PushedByPayload
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
        state = coordinate_holder.behaviour_state.get_copy(cls.name, BufferedMoverState)
        force = 1 if not isinstance(coordinate_holder, UnitProtocol) else coordinate_holder.stats.STR

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
                event_bus.publish(
                    Events.AnimationUpdate,
                    AnimationUpdatePayload(
                        coordinate_holder.name,
                        coordinate_holder.shape.get_textures()
                    )
                )

        coordinate_holder.behaviour_state.set(cls.name, state)

        return movement_utils.try_move(coordinate_holder, moving_direction, force) if moving_direction.is_not_zero() else True

    @classmethod
    @register_message_handler (MessageTypes.PUSHED_BY, for_=(CoordinateHolderProtocol,))
    def pushed_by(cls, coordinate_holder: CoordinateHolderProtocol, payload: PushedByPayload) -> bool:
        if payload.coordinates + payload.direction != coordinate_holder.coordinates:
            return True

        state = coordinate_holder.behaviour_state.get_copy(cls.name, BufferedMoverState)

        state.intent_velocity = CustomVec2f(
            payload.direction.x if payload.direction.x != 0 else state.intent_velocity.x,
            payload.direction.y if payload.direction.y != 0 else state.intent_velocity.y)

        state.clear_velocity = SimpleVec2Bool(
            True if payload.direction.x != 0 else state.clear_velocity.x,
            True if payload.direction.y != 0 else state.clear_velocity.y)

        state.intent_velocity_normalised = state.intent_velocity.normalized()
        if isinstance(coordinate_holder, UnitProtocol):
            state.intent_velocity_normalised *= coordinate_holder.stats.speed

        coordinate_holder.behaviour_state.set(cls.name, state)

        return True

    @classmethod
    @register_message_handler (MessageTypes.INTENTION_TO_MOVE, for_=(CoordinateHolderProtocol,))
    def intention_to_move(cls, coordinate_holder: CoordinateHolderProtocol, payload: MovePayload) -> bool:
        state = coordinate_holder.behaviour_state.get_copy(cls.name, BufferedMoverState)

        intent_velocity: list[float] = [state.intent_velocity.x, state.intent_velocity.y]
        clear_velocity: list[int] = [state.clear_velocity.x, state.clear_velocity.y]

        if payload.direction.x != 0:
            intent_velocity[0] = payload.direction.x
            clear_velocity[0] = 0

        if payload.direction.y != 0:
            intent_velocity[1] = payload.direction.y
            clear_velocity[1] = 0

        state.intent_velocity = CustomVec2f(*intent_velocity)
        state.clear_velocity = SimpleVec2Bool(*clear_velocity)

        state.intent_velocity_normalised = state.intent_velocity.normalized()
        if isinstance(coordinate_holder, UnitProtocol):
            state.intent_velocity_normalised *= coordinate_holder.stats.speed

        coordinate_holder.behaviour_state.set(cls.name, state)

        return True

    @classmethod
    @register_message_handler (MessageTypes.INTENTION_TO_STOP, for_=(CoordinateHolderProtocol,))
    def intention_to_stop(cls, coordinate_holder: CoordinateHolderProtocol, payload: StopPayload) -> bool:
        state = coordinate_holder.behaviour_state.get_copy(cls.name, BufferedMoverState)

        state.clear_velocity = SimpleVec2Bool(
            bool(state.clear_velocity.x or payload.direction.x),
            bool(state.clear_velocity.y or payload.direction.y),
        )

        coordinate_holder.behaviour_state.set(cls.name, state)

        return True
