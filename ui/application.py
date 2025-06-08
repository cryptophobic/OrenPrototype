import pygame

from engine.unit import Pawn
from event_processor.InputEvents import InputEvents, KeyPressDetails
from event_processor.Timer import Timer
from ui import config
from ui.actors.cursor.cursor import Cursor
from ui.actors.vectors import Vec2
from ui.state.state import State
from ui.renderer import Renderer
from engine.grid import Grid


class Application:
    def __init__(self, grid: Grid):
        self.grid = grid

        self.renderer = Renderer(self.grid)
        self.state_manager = State()
        self.event_dispatcher = InputEvents()
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


    def register_actors(self):
        cursor = Cursor(Vec2(0, 0))
        self.state_manager.register_actor(cursor)
        self.event_dispatcher.subscribe(cursor)

        pawn = Pawn(cursor)
        self.grid.place_unit(pawn)
        pass

    def run(self):
        render_threshold = self.ticker.last_timestamp + self.interval
        first_timestamp = self.ticker.last_timestamp
        self.register_actors()

        while not self.game_over:
            self.ticker.tick()
            self.check_exit()
            self.event_dispatcher.listen(self.ticker.last_timestamp)

            if self.ticker.last_timestamp >= render_threshold:
                render_threshold += self.interval
                events = self.event_dispatcher.slice_flat(first_timestamp, render_threshold)
                self.state_manager.update_state(events)
                first_timestamp = self.ticker.last_timestamp
                if self.state_manager.commit() is True:
                    self.renderer.draw()
