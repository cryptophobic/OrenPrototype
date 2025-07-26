from dataclasses import dataclass

from app.behaviours.behaviour import Behaviour, register_message_handler
from app.behaviours.types import BehaviourState
from app.core.vectors import CustomVec2f
from app.engine.message_broker.types import MessageTypes
from app.objects.coordinate_holder import CoordinateHolder


@register_message_handler(
    MessageTypes.ANIMATE,
    {
        CoordinateHolder: "move",
    }
)

@dataclass
class BufferedMoverState(BehaviourState):
    moving_buffer: CustomVec2f
    force: int = 0

class Animate(Behaviour):
    pass