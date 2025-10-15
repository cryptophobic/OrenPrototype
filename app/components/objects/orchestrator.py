from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.core.event_bus.consumer import Consumer
from app.core.event_bus.events import MousePositionUpdatePayload, Events
from app.core.types import ContinuousKeyPressEventLogRecords
from app.core.vectors import CustomVec2i
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, AnimatePayload, \
    InputPayload, IntentionToPlacePayload
from app.components.objects.actor import Actor
from app.components.objects.puppeteer import Puppeteer
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol
from app.protocols.collections.puppeteer_collection_protocol import PuppeteerCollectionProtocol
from app.protocols.objects.actor_protocol import ActorProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol
from app.protocols.objects.puppeteer_protocol import PuppeteerProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol


class Orchestrator(Actor, Consumer, OrchestratorProtocol):
    def __init__(self,
                 actors_collection: ActorCollectionProtocol[ActorProtocol],
                 messenger: MessageBrokerProtocol,
                 name: str = None):
        Actor.__init__(self, name=name)
        Consumer.__init__(self)
        self.delta_time: float = 0.0
        self.moveable_actors = actors_collection.get_behave_as_any([
            Behaviours.DISCRETE_MOVER,
            Behaviours.BUFFERED_MOVER,
        ])
        self.messenger = messenger
        self.actors_collection: ActorCollectionProtocol = actors_collection
        self._cursor: ActorProtocol = actors_collection.get_behave_as_this(Behaviours.CURSOR, True)
        self._cursor_position: CustomVec2i = CustomVec2i.zero()
        puppeteers = self.get_puppeteers()
        for puppeteer in puppeteers:
            self.puppeteer: PuppeteerProtocol = puppeteer
            break

        self.register_handler(Events.MousePositionUpdate, self._on_cursor_position_changed)

    def _on_cursor_position_changed(self, new_position: MousePositionUpdatePayload):
        if isinstance(self._cursor, CoordinateHolderProtocol):
            self._cursor_position = new_position.cell_position if self._cursor.coordinates != new_position.cell_position else None

    def get_puppeteers(self) -> PuppeteerCollectionProtocol:
        # TODO: replace with protocols later
        return self.actors_collection.get_active_actors().get_by_type(Puppeteer, PuppeteerCollection)

    def set_puppet(self, name: str) -> None:
        puppet = self.moveable_actors.get(name)
        self.puppeteer.puppet = puppet

    def process_continuous_input(self, key_press_input: dict[str, ContinuousKeyPressEventLogRecords]):
        for actor_name, log_records in key_press_input.items():
            if self.puppeteer:
                message = Message(
                    sender=self.name,
                    body=MessageBody(
                        message_type=MessageTypes.INPUT,
                        payload=InputPayload(actor_name=actor_name, input=sorted(log_records))
                    )
                )
                self.messenger.send_message(message, self.puppeteer)

    def _process_cursor_update(self):
        if self._cursor_position is not None:
            message = Message(
                sender=self.name,
                body=MessageBody(
                    message_type=MessageTypes.INTENTION_TO_PLACE,
                    payload=IntentionToPlacePayload(to_place=self._cursor_position)
                )
            )

            self.messenger.send_message(message, self._cursor)
            self._cursor_position = None

    def _process_animation(self):
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

    def _process_buffered_mover(self):
        buffered = self.actors_collection.get_active_actors().get_behave_as_this(Behaviours.BUFFERED_MOVER)
        for actor in buffered:
            state = actor.extract_behaviour_data(Behaviours.BUFFERED_MOVER)
            if state is None or (state.intent_velocity.is_zero() and state.moving_buffer.is_zero()):
                continue

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
        self._process_cursor_update()
        # self._process_animation()
        self._process_buffered_mover()
        self.delta_time = 0.0
