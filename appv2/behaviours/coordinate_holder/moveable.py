from ..behaviour import Behaviour, register_message_handler
from app.config import Behaviours
from ...bus.message_broker.types import MessageTypes, Message, PushedByPayload, Payload, MessageBody, \
    IntentionToMovePayload
from ...context.message_broker_context import MessageBrokerContext
from ...helpers.vectors import Vec2
from ...protocols.coordinate_holder_protocol import CoordinateHolderProtocol, UnitProtocol

if TYPE_CHECKING:
    from ...objects.actor.coordinate_holder import CoordinateHolder
    from ...objects.actor.unit import Unit


@register_message_handler(
    MessageTypes.PUSHED_BY,
    {
        UnitProtocol: "pushed_by_as_unit",
        CoordinateHolderProtocol: "pushed_by_as_coordinate_holder",
    }
)

@register_message_handler(
    MessageTypes.INTENTION_TO_MOVE,
    {
        UnitProtocol: "intention_to_move_as_unit",
        CoordinateHolderProtocol: "intention_to_move_as_coordinate_holder",
    }
)

class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    supported_receivers = (CoordinateHolderProtocol, UnitProtocol)

    '''
    internal implementation of behavioural actions
    '''
    @classmethod
    def __move(cls, coordinate_holder: CoordinateHolderProtocol, direction: Vec2, force: int) -> bool:
        result = cls.context.move_coordinate_holder(coordinate_holder, coordinate_holder.coordinates + direction)
        broker_context = MessageBrokerContext().instance().context
        for actor in result.blocked.values():
            message = Message(
                sender=coordinate_holder,
                body=MessageBody(
                    message_type=MessageTypes.PUSHED_BY,
                    payload=PushedByPayload(
                        direction=direction,
                        force=force,
                    )
                )
            )
            message_id = broker_context.send_message(message, actor)
            if message_id is not None:
                response_actions = broker_context.get_response(message_id)
                coordinate_holder.pending_actions.extend(response_actions)

        for actor in result.overlapped.values():
            message = Message(
                sender=coordinate_holder,
                body=MessageBody(
                    message_type=MessageTypes.OVERLAPPED_BY,
                    payload=Payload(),
                )
            )
            broker_context.send_message(message=message, responder=actor, no_response=True)

        return result.placed


    '''
    Handlers to execute by command pipeline
    '''
    @classmethod
    def pushed_by_as_unit(cls, unit: UnitProtocol, pushed_payload: PushedByPayload) -> bool:
        return cls.pushed_by_as_coordinate_holder(unit, pushed_payload)

    @classmethod
    def pushed_by_as_coordinate_holder(cls, coordinate_holder: CoordinateHolderProtocol, pushed_payload: PushedByPayload) -> bool:
        if pushed_payload.force > 0:
            return cls.__move(coordinate_holder, pushed_payload.direction, pushed_payload.force - 1)
        else:
            return True

    @classmethod
    def intention_to_move_as_unit(cls, unit: UnitProtocol, intention_to_move_payload: IntentionToMovePayload) -> bool:
        return cls.__move(
            coordinate_holder=unit,
            direction=intention_to_move_payload.direction,
            force=unit.stats.STR
        )

    @classmethod
    def intention_to_move_as_coordinate_holder(cls, coordinate_holder: CoordinateHolderProtocol, intention_to_move_payload: PushedByPayload) -> bool:
        return cls.__move(
            coordinate_holder=coordinate_holder,
            direction=intention_to_move_payload.direction,
            force=1
        )
