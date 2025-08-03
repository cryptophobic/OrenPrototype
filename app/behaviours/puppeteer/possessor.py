from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, ControlsPayload, Message, InputPayload
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

@register_message_handler(
    MessageTypes.INPUT,
    {
        PuppeteerProtocol: "on_input",
    }
)

class Possessor(Behaviour):
    name = Behaviours.POSSESSOR
    supported_receivers = (PuppeteerProtocol,)

    @classmethod
    def __key_process(cls, puppeteer: PuppeteerProtocol, payload: ControlsPayload, is_down: bool) -> bool:
        if not isinstance(payload, ControlsPayload):
            raise TypeError(f"Expected ControlsPayload, got {type(payload)}")

        key_code = payload.key_code
        binding = puppeteer.controls.get(key_code)
        mapped = binding.key_down if is_down else binding.key_up

        if not mapped:
            return False

        forward = Message(sender=puppeteer.name, body=mapped)
        messenger = cls.get_messenger()
        messenger.send_message(forward, puppeteer.puppet)

        return True


    @classmethod
    def _on_input_process(cls, puppeteer: PuppeteerProtocol, payload: InputPayload) -> bool:
        if puppeteer.name != payload.actor_name:
            print(f"puppeteer name is not recognised: {payload.actor_name} vs {puppeteer.name}")
            return False

        for event in payload.input:
            key_code = event.key
            binding = puppeteer.controls.get(key_code)

            message = binding.key_down if event.down else binding.key_up
            if not message:
                continue

            forward = Message(sender=puppeteer.name, body=message)
            messenger = cls.get_messenger()
            messenger.send_message(forward, puppeteer.puppet)

        return True

    @classmethod
    def key_down(cls, puppeteer: PuppeteerProtocol, payload: ControlsPayload) -> bool:
        print(f"key_down: {payload}")
        return True
        # return cls.__key_process(puppeteer, payload, is_down=True)

    @classmethod
    def key_up(cls, puppeteer: PuppeteerProtocol, payload: ControlsPayload) -> bool:
        return True
        # return cls.__key_process(puppeteer, payload, is_down=False)

    @classmethod
    def on_input(cls, puppeteer: PuppeteerProtocol, payload: InputPayload) -> bool:
        print(f"on_input: {payload}")
        return cls._on_input_process(puppeteer, payload)