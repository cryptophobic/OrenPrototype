from appv2.engine.message_broker.types import Controls
from appv2.objects.actor import Actor
from appv2.protocols.objects.puppeteer_protocol import PuppeteerProtocol


class Puppeteer(Actor, PuppeteerProtocol):
    def __init__(self, puppet: Actor, controls: Controls, name: str = None):
        super().__init__(name)

        self.puppet = puppet
        self.controls = controls
