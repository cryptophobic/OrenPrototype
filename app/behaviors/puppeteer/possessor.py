from collections import deque

from ..behaviour import Behaviour, BehaviourAction
from ...bus.message_broker.types import MessageBody, ControlsPayload, MessageTypes, Message
from ...config import Behaviours
from ...context.message_broker_context import MessageBrokerContext
from ...objects.actor.puppeteer import Puppeteer


class Possessor(Behaviour):
    name = Behaviours.POSSESSOR
    supported_receivers = (Puppeteer,)

    @classmethod
    def __key_process(cls, puppeteer: Puppeteer, message_body: MessageBody, is_down: bool) -> deque[BehaviourAction]:
        if not isinstance(message_body.payload, ControlsPayload):
            raise TypeError(f"Expected ControlsPayload, got {type(message_body.payload)}")

        key_code = message_body.payload.key_code
        binding = puppeteer.controls.get(key_code)
        mapped = binding.key_down if is_down else binding.key_up

        if not mapped:
            return deque()

        forward = Message(sender=puppeteer, body=mapped)
        broker = MessageBrokerContext().instance().context
        msg_id = broker.send_message(forward, puppeteer.puppet)
        if msg_id:
            promise = broker.get_response(msg_id)
            puppeteer.pending_actions.extend(promise.response_actions)

        return deque()

    @classmethod
    def on_key_down(cls, puppeteer: Puppeteer, message_body: MessageBody) -> deque[BehaviourAction]:
        return cls.__key_process(puppeteer, message_body, is_down=True)

    @classmethod
    def on_key_up(cls, puppeteer: Puppeteer, message_body: MessageBody) -> deque[BehaviourAction]:
        return cls.__key_process(puppeteer, message_body, is_down=False)

    @classmethod
    def register_handlers(cls):
        existing = cls.message_handlers.get(MessageTypes.KEY_DOWN, ()) + cls.message_handlers.get(MessageTypes.KEY_UP, ())
        cls.message_handlers[MessageTypes.KEY_DOWN] = existing + (cls.on_key_down,)
        cls.message_handlers[MessageTypes.KEY_UP] = existing + (cls.on_key_up,)


