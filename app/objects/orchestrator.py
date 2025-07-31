from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.core.types import KeyPressEventLogRecords
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, ControlsPayload, AnimatePayload
from app.objects.actor import Actor
from app.objects.puppeteer import Puppeteer
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol



class Orchestrator(Actor, OrchestratorProtocol):
    def __init__(self,
                 actors_collection: ActorCollectionProtocol[ActorProtocol],
                 messenger: MessageBrokerProtocol,
                 name: str = None):
        super().__init__(name)
        self.delta_time: float = 0.0
        self.moveable_actors = actors_collection.get_behave_as_this(Behaviours.DISCRETE_MOVER)
        self.messenger = messenger
        self.actors_collection: ActorCollectionProtocol = actors_collection
        puppeteers = self.get_puppeteers()
        for puppeteer in puppeteers:
            self.puppeteer: PuppeteerProtocol = puppeteer
            break

    def get_puppeteers(self) -> PuppeteerCollectionProtocol:
        # TODO: replace with protocols later
        return self.actors_collection.get_by_type(Puppeteer, PuppeteerCollection)

    def set_puppet(self, name: str) -> None:
        puppet = self.moveable_actors.get(name)
        self.puppeteer.puppet = puppet

    def process_input(self, keys_down: list[int], key_press_input: KeyPressEventLogRecords):



        for log_record in key_press_input:
            if self.puppeteer:
                message = Message(
                    sender=self.name,
                    body=MessageBody(
                        message_type=MessageTypes.KEY_DOWN if log_record.down is True else MessageTypes.KEY_UP,
                        payload=ControlsPayload(key_code=log_record.key)
                    )
                )
                self.messenger.send_message(message, self.puppeteer)

    def __process_animation(self):
        animated = self.actors_collection.get_behave_as_this(Behaviours.ANIMATED)
        for actor in animated:
            message = Message(
                sender=self.name,
                body=MessageBody(
                    message_type=MessageTypes.ANIMATE,
                    payload=AnimatePayload(delta_time=self.delta_time)
                )
            )
            self.messenger.send_message(message, actor)

    def __process_buffered_mover(self):
        buffered = self.actors_collection.get_behave_as_this(Behaviours.BUFFERED_MOVER)
        for actor in buffered:
            message = Message(
                sender=self.name,
                body=MessageBody(
                    message_type=MessageTypes.BUFFERED_MOVE,
                    payload=AnimatePayload(delta_time=self.delta_time)
                )
            )
            self.messenger.send_message(message, actor)

    def process_tick(self, delta_time: float):
        self.delta_time += delta_time
        self.__process_animation()
        self.__process_buffered_mover()
        self.delta_time = 0.0


