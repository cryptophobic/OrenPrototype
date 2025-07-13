import pygame

from app import config
from app.engine.context.game_context import GameContext
from app.engine.input_processor.InputEvents import InputEvents
from app.engine.input_processor.Timer import Timer
from app.maps.level1 import LevelFactory
from app.renderer import Renderer


class Application:
    def __init__(self):
        self.renderer = Renderer()
        self.level_factory = LevelFactory()
        self.renderer.grid = self.level_factory.levels["level1"].grid

        self.context = GameContext()

        # Initialize core systems
        # self.state_manager = StateManager()
        # self.supervisor = Supervisor(self.state_manager)
        self.event_dispatcher = InputEvents()
        self.ticker = Timer()

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

    def run(self):
        """Main game loop"""
        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp
        # self.register_actors()

        while not self.game_over:
            self.ticker.tick()
            # self.frame_context.timestamp = self.ticker.last_timestamp
            self.check_exit()
            # self.event_dispatcher.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval

                # NEW: Supervisor runs first
                # self.supervisor.update()

                # Get events and update state
                events = self.event_dispatcher.slice_flat(first_timestamp, render_threshold)
                # self.state_manager.update_state(events)
                first_timestamp = self.ticker.last_timestamp

                # Render if state changed
                # if self.state_manager.commit():
                #     self.renderer.draw()

                if True:
                    self.renderer.draw()

        pygame.quit()