from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, Message, InputPayload
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol

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
    def on_input(cls, puppeteer: PuppeteerProtocol, payload: InputPayload) -> bool:
        return cls._on_input_process(puppeteer, payload)