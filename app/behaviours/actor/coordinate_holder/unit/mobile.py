from dataclasses import dataclass
from typing import cast

from app.behaviours.behaviour import register_message_handler, Behaviour
from app.behaviours.types import BehaviourState
from app.config import Behaviours
from app.core.vectors import CustomVec2f
from app.engine.message_broker.types import MessageTypes, PushedByPayload, IntentionToMovePayload, AnimatePayload
from app.protocols.objects.unit_protocol import UnitProtocol


@register_message_handler(
    MessageTypes.ANIMATE,
    {
        UnitProtocol: "animate",
    }
)

@dataclass
class MobileState(BehaviourState):
    moving_buffer: CustomVec2f = CustomVec2f(0.0, 0.0)

class Mobile(Behaviour):
    name = Behaviours.MOBILE
    supported_receivers = (UnitProtocol,)

    '''
    internal implementation of behavioural actions
    '''
    @classmethod
    def __animate(cls, unit: UnitProtocol, payload: AnimatePayload) -> bool:
        state = cast(MobileState, unit.behaviour_state.get(cls.name)) # type: MobileState

        state.moving_buffer += unit.velocity * payload.delta_time
        candidate = CustomVec2f(unit.coordinates.x, unit.coordinates.y)


        return True



    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def pushed_by(cls, unit: UnitProtocol, payload: PushedByPayload) -> bool:
        return cls.__move(unit, payload.direction, payload.force - 1)

    @classmethod
    def intention_to_move(cls, unit: UnitProtocol, payload: IntentionToMovePayload) -> bool:
        return cls.__move(
            coordinate_holder=unit,
            direction=payload.direction,
            force=unit.stats.STR
        )
