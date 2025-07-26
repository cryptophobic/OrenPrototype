from dataclasses import dataclass

from app.behaviours.actor.coordinate_holder.moveable import Moveable
from app.behaviours.behaviour import register_message_handler
from app.behaviours.types import BehaviourState
from app.config import Behaviours
from app.core.vectors import CustomVec2f
from app.engine.message_broker.types import MessageTypes, AnimatePayload, SetVelocityPayload
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.ANIMATE,
    {
        UnitProtocol: "animate",
    }
)

@dataclass
class AnimatedMoverState(BehaviourState):
    moving_buffer: CustomVec2f
    force: int = 0

class AnimatedMover(Moveable):
    name = Behaviours.ANIMATED_MOVER
    supported_receivers = (UnitProtocol,)

    '''
    internal implementation of behavioural actions
    '''
    @classmethod
    def __animate(cls, unit: UnitProtocol, payload: AnimatePayload) -> bool:
        state = unit.behaviour_state.get(cls.name)

        if (not isinstance(state, AnimatedMoverState) or state.moving_buffer.is_zero()) and unit.velocity.is_zero():
            unit.behaviour_state.pop(cls.name, None)
            return True

        if not isinstance(state, AnimatedMoverState):
            unit.behaviour_state[cls.name] = AnimatedMoverState(
                moving_buffer=CustomVec2f(0.0, 0.0),
                force=unit.stats.STR,
            )
            state = unit.behaviour_state.get(cls.name)

        state.moving_buffer += unit.velocity * payload.delta_time
        direction = CustomVec2f.zero()

        for n in [0, 1]:
            if abs(state.moving_buffer[n]) >= 1:
                step = int(state.moving_buffer[n])
                direction[n] += step
                state.moving_buffer[n] -= step

        return cls.get_movement_utils().try_move(unit, direction, state.force) if direction.is_not_zero() else True

    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def animate(cls, unit: UnitProtocol, payload: AnimatePayload) -> bool:
        return cls.__animate(unit, payload)

    @classmethod
    def intention_to_move(cls, unit: UnitProtocol, payload: SetVelocityPayload) -> bool:
        unit.velocity += payload.velocity
        return True
