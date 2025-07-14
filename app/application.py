import pygame

from app import config
from app.collections.puppeteer_collection import PuppeteerCollection
from app.config import Behaviours
from app.engine.command_pipeline.pipeline import CommandPipeline
from app.engine.context.game_context import GameContext
from app.engine.input_processor.InputEvents import InputEvents
from app.engine.input_processor.Timer import Timer
from app.engine.message_broker.broker import MessageBroker
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, InputPayload
from app.maps.level1 import LevelFactory
from app.objects.orchestrator import Orchestrator
from app.objects.puppeteer import Puppeteer
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol
from app.registry.behaviour_registry import get_registry
from app.renderer import Renderer


class Application:
    def __init__(self):
        self.renderer = Renderer()
        self.level_factory = LevelFactory()
        self.current_level = self.level_factory.levels["level1"]
        self.renderer.grid = self.current_level.grid
        self.context = GameContext()
        self.event_dispatcher = InputEvents()
        self.message_broker = MessageBroker()
        self.command_pipeline = CommandPipeline()

        # Initialize core systems
        self.orchestrator: OrchestratorProtocol = Orchestrator(self.current_level.actors_collection)
        self.orchestrator.behaviours.set(Behaviours.INPUT_HANDLER)

        self.ticker = Timer()

        self.i = 0
        self.pressed = False

        # Game loop settings
        self.interval = 1000 / config.FPS
        self.game_over = False

    def check_exit(self):
        """Check for exit conditions"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game_over = True

    def switch(self, puppets):
        pressed = pygame.key.get_pressed()
        length = len(puppets)
        if pressed[pygame.K_TAB] and not self.pressed:
            self.pressed = True
            print(self.i, length, self.i % length)
            self.orchestrator.set_puppet(puppets[self.i % length].name)
            self.i += 1
        else:
            self.pressed = pressed[pygame.K_TAB]



    def register_actors(self):
        for puppeteer in self.orchestrator.actors_collection.get_by_type(Puppeteer, PuppeteerCollection):
            self.event_dispatcher.subscribe(puppeteer.name, puppeteer.controls)

    def run(self):
        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp
        self.register_actors()
        self.renderer.draw()
        self.command_pipeline.actor_collection = self.orchestrator.actors_collection
        base_behaviour = get_registry().get(Behaviours.BEHAVIOUR)
        base_behaviour.register_grid(self.current_level.grid)
        base_behaviour.register_messenger(self.message_broker)

        puppets = list(self.orchestrator.moveable_actors.raw_items().values())

        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.switch(puppets)
            self.event_dispatcher.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval
                events = self.event_dispatcher.slice_flat(first_timestamp, render_threshold)

                if not events:
                    continue

                # TODO: Maybe later move this logic to some behaviour as currently only behaviours sending messages
                message = Message(
                    sender="Application",
                    body=MessageBody(
                        message_type=MessageTypes.INPUT,
                        payload=InputPayload(events),
                    )
                )
                _, pending_actions = self.message_broker.send_message(message, self.orchestrator)
                self.orchestrator.pending_actions.extend(pending_actions)

                # TODO: think twice if it is logical enough to pass self.orchestrator
                state_changed = self.command_pipeline.process(self.orchestrator)

                first_timestamp = self.ticker.last_timestamp
                self.context.tick()

                if state_changed:
                    self.renderer.draw()
        # TODO: graceful exit with save states
        pygame.quit()