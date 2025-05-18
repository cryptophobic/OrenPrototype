import pygame
from ui.input import InputHandler
from ui.renderer import Renderer
from engine.grid import Grid


class Interaction:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.renderer = Renderer(self.grid)
        self.input = InputHandler()
        self.selected_x = 0
        self.selected_y = 0

    def update(self):
        self.input.poll()
        dx, dy = self.input.get_direction()

        if dx != 0 or dy != 0:
            self.move_selection(dx, dy)

        if self.input.enter_pressed:
            self.interact()

        self.renderer.draw((self.selected_x, self.selected_y))

    def move_selection(self, dx, dy):
        new_x = max(0, min(self.grid.width - 1, self.selected_x + dx))
        new_y = max(0, min(self.grid.height - 1, self.selected_y + dy))
        self.selected_x = new_x
        self.selected_y = new_y

    def interact(self):
        cell = self.grid.get_cell(self.selected_x, self.selected_y)
        print(f"Interacted with Cell ({cell.x}, {cell.y}) — Obstacle: {cell.obstacle}, Unit: {cell.unit}")
