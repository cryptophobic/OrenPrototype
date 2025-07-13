from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, MessageBody, ControlsPayload, Message
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol


@register_message_handler(
    MessageTypes.KEY_DOWN,
    {
        PuppeteerProtocol: "key_down",
    }
)

@register_message_handler(
    MessageTypes.KEY_UP,
    {
        PuppeteerProtocol: "key_up",
    }
)


class Possessor(Behaviour):
    name = Behaviours.POSSESSOR
    supported_receivers = (PuppeteerProtocol,)

    @classmethod
    def __key_process(cls, puppeteer: PuppeteerProtocol, message_body: MessageBody, is_down: bool) -> bool:
        if not isinstance(message_body.payload, ControlsPayload):
            raise TypeError(f"Expected ControlsPayload, got {type(message_body.payload)}")

        key_code = message_body.payload.key_code
        binding = puppeteer.controls.get(key_code)
        mapped = binding.key_down if is_down else binding.key_up

        if not mapped:
            return False

        forward = Message(sender=puppeteer.name, body=mapped)
        messenger = cls.get_messenger()
        _, response_actions = messenger.send_message(forward, puppeteer.puppet)
        if response_actions:
            puppeteer.pending_actions.extend(response_actions)

        return True

    @classmethod
    def key_down(cls, puppeteer: PuppeteerProtocol, message_body: MessageBody) -> bool:
        return cls.__key_process(puppeteer, message_body, is_down=True)

    @classmethod
    def key_up(cls, puppeteer: PuppeteerProtocol, message_body: MessageBody) -> bool:
        return cls.__key_process(puppeteer, message_body, is_down=False)
