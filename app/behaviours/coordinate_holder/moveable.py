from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.core.vectors import Vec2
from app.engine.message_broker.types import MessageTypes, Message, MessageBody, PushedByPayload, Payload, \
    IntentionToMovePayload
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol


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
        result = cls.get_grid().move(coordinate_holder, coordinate_holder.coordinates + direction)
        messenger = cls.get_messenger()
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
            _, response_actions = messenger.send_message(message, actor)
            if response_actions is not None:
                coordinate_holder.pending_actions.extend(response_actions)

        for actor in result.overlapped:
            message = Message(
                sender=coordinate_holder.name,
                body=MessageBody(
                    message_type=MessageTypes.OVERLAPPED_BY,
                    payload=Payload(),
                )
            )
            messenger.send_message(message=message, responder=actor)

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
