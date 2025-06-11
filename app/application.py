import pygame

from .context.context import Context
from .event_processor.InputEvents import InputEvents
from .event_processor.Timer import Timer
from .engine.state.grid import Grid
from .engine.state.state_manager import StateManager
from .engine.supervisor.supervisor import Supervisor
from .renderer import Renderer
import config


class Application:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create 10x15 empty grid as requested
        self.grid = Grid(10, 15)

        # Initialize core systems
        self.state_manager = StateManager(self.grid)
        self.supervisor = Supervisor(self.state_manager)
        self.event_dispatcher = InputEvents()
        self.ticker = Timer()
        self.context = Context.instance()
        self.renderer = Renderer(self.grid)
        
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

    def register_actors(self):
        """Register initial actors (placeholder for now)"""
        # For now, just subscribe to some basic keys for testing
        # This will be replaced by proper Actor registration later
        test_keys = [(pygame.K_UP, 100), (pygame.K_DOWN, 100), (pygame.K_LEFT, 100), (pygame.K_RIGHT, 100)]
        self.event_dispatcher.subscribe("test_actor", test_keys)

    def run(self):
        """Main game loop"""
        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp
        self.register_actors()

        while not self.game_over:
            self.ticker.tick()
            self.context.frame_context.timestamp = self.ticker.last_timestamp
            self.check_exit()
            self.event_dispatcher.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval
                
                # NEW: Supervisor runs first
                self.supervisor.update()
                
                # Get events and update state
                events = self.event_dispatcher.slice_flat(first_timestamp, render_threshold)
                self.state_manager.update_state(events)
                first_timestamp = self.ticker.last_timestamp
                
                # Render if state changed
                if self.state_manager.commit():
                    self.renderer.draw()

        pygame.quit()