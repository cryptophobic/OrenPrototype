import pygame
from deprecated.engine.grid import Grid
from deprecated.ui import config
from deprecated.ui.actors.vectors import Vec2

GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (50, 50, 50)

class Renderer:
    def __init__(self, grid: Grid):
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("Hello Oren")
        self.grid = grid
        self.tile_size = {
            "x": config.SCREEN_SIZE[0] // grid.width,
            "y": config.SCREEN_SIZE[1] // grid.height,
        }
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(Vec2(x, y))
                rect = pygame.Rect(x * self.tile_size["x"], y * self.tile_size["y"], self.tile_size["x"], self.tile_size["x"])
                pygame.draw.rect(self.screen, GRID_COLOR, rect)

                if cell.unit:
                    actor = cell.unit.actor
                    icon = actor.body.shape.icon
                    scaled_icon = pygame.transform.scale(icon, (self.tile_size["x"], self.tile_size["y"]))
                    # Create a display surface

                    # Draw it on screen (at position 100,100)
                    self.screen.blit(scaled_icon, (x * self.tile_size["x"], y * self.tile_size["y"]))

                if cell.selected:
                    pygame.draw.rect(self.screen, SELECTED_COLOR, rect, 2)  # highlight

                pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)  # grid border

        pygame.display.flip()
