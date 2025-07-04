from collections import deque
from typing import Optional

from ..behaviour import Behaviour, BehaviourAction
from app.config import Behaviours
from ...bus.message_broker.types import MessageTypes, Message, PushedByPayload, Payload
from ...context.message_broker_context import MessageBrokerContext
from ...helpers.vectors import Vec2
from ...objects.actor.coordinate_holder import CoordinateHolder
from ...objects.actor.static_object import StaticObject
from ...objects.actor.unit import Unit


class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    supported_receivers = (CoordinateHolder, StaticObject, Unit)

    @classmethod
    def move(cls, coordinate_holder: CoordinateHolder, direction: Vec2, force: int) -> bool:
        result = cls.context.move_coordinate_holder(coordinate_holder, coordinate_holder.coordinates + direction)
        broker_context = MessageBrokerContext().instance().context
        for actor in result.blocked.values():
            message = Message(
                sender=coordinate_holder,
                message_type=MessageTypes.PUSHED_BY,
                payload=PushedByPayload(
                    direction=direction,
                    force=force,
                )
            )
            message_id = broker_context.send_message(message, actor)
            if message_id is not None:
                promise = broker_context.get_response(message_id)
                coordinate_holder.blocking_actions.extend(promise.response_actions)

        for actor in result.overlapped.values():
            message = Message(
                sender=coordinate_holder,
                message_type=MessageTypes.OVERLAPPED_BY,
                payload=Payload()
            )
            broker_context.send_message(message=message, responder=actor, no_response=True)

        return result

    @classmethod
    def handle_pushed_by_as_unit(cls, unit: Unit, pushed_payload: PushedByPayload) -> bool:
        pass

    @classmethod
    def handle_pushed_by_as_coordinate_holder(cls, coordinate_holder: CoordinateHolder, pushed_payload: PushedByPayload) -> bool:
        if pushed_payload.force > 0:
            return cls.move(coordinate_holder, pushed_payload.direction, pushed_payload.force - 1)
        else:
            return True


    @classmethod
    def handle_pushed_by_as_static_object(cls, static_object: StaticObject, pushed_payload: PushedByPayload) -> bool:
        pass

    @classmethod
    def pushed_by(cls, receiver: CoordinateHolder, message: Message) -> Optional[deque[BehaviourAction]]:
        if not isinstance(message.payload, PushedByPayload):
            raise TypeError(f"Expected PushedByPayload, got {type(message.payload)}")

        actions_queue: deque[BehaviourAction] = deque()

        if isinstance(receiver, Unit):
            actions_queue.append(
                BehaviourAction(
                    behaviour=Behaviours.MOVEABLE,
                    method_name="handle_pushed_by_as_unit",
                    kwargs=message.payload.__dict__
                )
            )

        if isinstance(receiver, StaticObject):
            actions_queue.append(
                BehaviourAction(
                    behaviour=Behaviours.MOVEABLE,
                    method_name="handle_pushed_by_as_static_object",
                    kwargs=message.payload.__dict__
                )
            )

        if isinstance(receiver, CoordinateHolder):
            actions_queue.append(
                BehaviourAction(
                    behaviour=Behaviours.MOVEABLE,
                    method_name="handle_pushed_by_as_coordinate_holder",
                    kwargs=message.payload.__dict__
                )
            )

        return actions_queue

    @classmethod
    def register_handlers(cls):
        existing = cls.message_handlers.get(MessageTypes.PUSHED_BY, ())
        cls.message_handlers[MessageTypes.PUSHED_BY] = existing + (cls.pushed_by,)
