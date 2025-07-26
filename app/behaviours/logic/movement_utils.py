from app.core.vectors import CustomVec2i
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, PushedByPayload, Payload
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol


class MovementUtils:
    
    def __init__(self, grid: GridProtocol, messenger: MessageBrokerProtocol):
        self._grid = grid
        self._messenger = messenger

    def try_move(self, coordinate_holder, direction: CustomVec2i, force: int) -> bool:

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
            _, response_actions = self._messenger.send_message(message, actor)
            if response_actions:
                actor.pending_actions.extend(response_actions)

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

