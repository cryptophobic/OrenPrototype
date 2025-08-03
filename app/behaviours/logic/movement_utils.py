from app.behaviours.types import BufferedMoverState
from app.core.vectors import CustomVec2i
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, PushedByPayload, Payload
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol


class MovementUtils:
    
    def __init__(self, grid: GridProtocol, messenger: MessageBrokerProtocol):
        self._grid = grid
        self._messenger = messenger

    @staticmethod
    def calculate_buffered_move(
            coordinate_holder: CoordinateHolderProtocol,
            state: BufferedMoverState,
            delta_time: float
    ) -> tuple[BufferedMoverState, CustomVec2i]:
        state.moving_buffer += (coordinate_holder.velocity + coordinate_holder.intent_velocity) * delta_time
        direction = CustomVec2i.zero()

        if abs(state.moving_buffer.x) >= 1.0:
            step = int(state.moving_buffer.x)
            direction.x += step
            state.moving_buffer.x -= step
            if state.clear_velocity.x:
                state.moving_buffer.x = 0.0
                state.intent_velocity.x = 0.0

        if abs(state.moving_buffer.y) >= 1.0:
            step = int(state.moving_buffer.y)
            direction.y += step
            state.moving_buffer.y -= step
            if state.clear_velocity.y:
                state.moving_buffer.y = 0.0
                state.intent_velocity.y = 0.0

        return state, direction

    def try_move(self, coordinate_holder: CoordinateHolderProtocol, direction: CustomVec2i, force: int) -> bool:

        result = self._grid.move(coordinate_holder, coordinate_holder.coordinates + direction)

        for actor in result.blocked:
            message = Message(
                sender=coordinate_holder.name,
                body=MessageBody(
                    message_type=MessageTypes.PUSHED_BY,
                    payload=PushedByPayload(
                        direction=direction,
                        force=force,
                    )
                )
            )
            self._messenger.send_message(message, actor)

        for actor in result.overlapped:
            message = Message(
                sender=coordinate_holder.name,
                body=MessageBody(
                    message_type=MessageTypes.OVERLAPPED_BY,
                    payload=Payload(),
                )
            )
            self._messenger.send_message(message=message, responder=actor)

        return result.placed

