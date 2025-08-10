from app.behaviours.behaviour import Behaviour, register_message_handler
from app.config import Behaviours
from app.engine.message_broker.types import MessageTypes, Message, InputPayload
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol

class Possessor(Behaviour):
    name = Behaviours.POSSESSOR
    supported_receivers = (PuppeteerProtocol,)

    @classmethod
    @register_message_handler (MessageTypes.INPUT, for_=(PuppeteerProtocol,))
    def on_input(cls, puppeteer: PuppeteerProtocol, payload: InputPayload) -> bool:
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
