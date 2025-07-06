from collections import deque

from ..behaviour import Behaviour, BehaviourAction, register_message_handler
from ...bus.message_broker.types import MessageBody, ControlsPayload, MessageTypes, Message
from ...config import Behaviours
from ...context.message_broker_context import MessageBrokerContext
from ...objects.actor.puppeteer import Puppeteer

@register_message_handler(
    MessageTypes.KEY_DOWN,
    {
        Puppeteer: "key_down",
    }
)

@register_message_handler(
    MessageTypes.KEY_UP,
    {
        Puppeteer: "key_up",
    }
)


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
            response_actions = broker.get_response(msg_id)
            puppeteer.pending_actions.extend(response_actions)

        return deque()

    @classmethod
    def key_down(cls, puppeteer: Puppeteer, message_body: MessageBody) -> deque[BehaviourAction]:
        return cls.__key_process(puppeteer, message_body, is_down=True)

    @classmethod
    def key_up(cls, puppeteer: Puppeteer, message_body: MessageBody) -> deque[BehaviourAction]:
        return cls.__key_process(puppeteer, message_body, is_down=False)
