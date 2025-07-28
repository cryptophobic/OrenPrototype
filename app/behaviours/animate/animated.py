from dataclasses import dataclass

from app.behaviours.behaviour import Behaviour, register_message_handler
from app.behaviours.types import BehaviourState
from app.engine.message_broker.types import MessageTypes, AnimatePayload
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


@register_message_handler(
    MessageTypes.ANIMATE,
    {
        CoordinateHolder: "animate",
    }
)

@dataclass
class AnimatedState(BehaviourState):
    aggregated_delta: float = 0.0
    threshold: float = 0.1


class Animated(Behaviour):

    @classmethod
    def animate(cls, coordinate_holder: CoordinateHolderProtocol, payload: AnimatePayload) -> bool:
        state = coordinate_holder.behaviour_state.get(cls.name)

        if not isinstance(state, AnimatedState):
            state = AnimatedState()

        state.aggregated_delta += payload.delta_time
        if state.aggregated_delta > state.threshold:



        return True
