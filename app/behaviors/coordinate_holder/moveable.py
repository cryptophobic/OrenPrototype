from collections import deque
from typing import Optional

from ..behaviour import Behaviour, BehaviourAction
from app.config import Behaviours
from ...bus.message_broker.types import MessageTypes, Message, PushedByPayload
from ...objects.actor.coordinate_holder import CoordinateHolder
from ...objects.actor.static_object import StaticObject
from ...objects.actor.unit import Unit


class Moveable(Behaviour):
    name = Behaviours.MOVEABLE
    supported_receivers = (CoordinateHolder, StaticObject, Unit)

    @classmethod
    def handle_pushed_by_as_unit(cls, unit: Unit, pushed_payload: PushedByPayload) -> BehaviourAction:
        pass

    @classmethod
    def handle_pushed_by_as_coordinate_holder(cls, unit: CoordinateHolder, pushed_payload: PushedByPayload) -> BehaviourAction:
        pass

    @classmethod
    def handle_pushed_by_as_static_object(cls, unit: StaticObject, pushed_payload: PushedByPayload) -> BehaviourAction:
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
