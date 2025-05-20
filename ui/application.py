import pygame

from event_processor.InputEvents import InputEvents, KeyPressDetails
from event_processor.Timer import Timer
from ui import config
from ui.state.state import State
from ui.renderer import Renderer
from engine.grid import Grid


class Application:
    def __init__(self, grid: Grid):
        self.grid = grid

        self.renderer = Renderer(self.grid)
        self.state_manager = State()
        self.event_processor = InputEvents()
        self.ticker = Timer()

        self.interval = 1000 / config.FPS
        self.game_over = False
        self.selected_x = 0
        self.selected_y = 0

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game_over = True


    def init_events(self):
        self.event_processor.subscribe('Player1', [
            KeyPressDetails(pygame.K_UP, 150),
            KeyPressDetails(pygame.K_DOWN, 150),
            KeyPressDetails(pygame.K_LEFT, 150),
            KeyPressDetails(pygame.K_RIGHT, 150),
            KeyPressDetails(pygame.K_KP_ENTER, -1),
        ])

    def run(self):

        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp

        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.event_processor.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval
                events = self.event_processor.slice(first_timestamp, render_threshold)
                self.state_manager.update_state(events)
                first_timestamp = self.ticker.last_timestamp
                if self.state_manager.commit() is True:
                    self.renderer.draw()
