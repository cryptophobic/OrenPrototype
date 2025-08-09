from typing import Protocol

from app.core.vectors import CustomVec2f
from app.protocols.behaviours.readonly_behaviour_state_protocol import ReadonlyBehaviourStateProtocol


class ReadOnlyBufferedMoverStateProtocol(ReadonlyBehaviourStateProtocol, Protocol):
    @property
    def moving_buffer(self) -> CustomVec2f: ...
