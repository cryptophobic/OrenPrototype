import pygame
from engine.grid import Grid

GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (50, 50, 50)
SCREEN_SIZE = (1000, 800)

class Renderer:
    def __init__(self, grid: Grid):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("Hello Oren")
        self.grid = grid
        self.tile_size = {
            "x": SCREEN_SIZE[0] // grid.width,
            "y": SCREEN_SIZE[1] // grid.height,
        }
        self.screen.fill((0, 0, 0))

    def draw(self, selected_pos):
        self.screen.fill((0, 0, 0))
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                rect = pygame.Rect(x * self.tile_size["x"], y * self.tile_size["y"], self.tile_size["x"], self.tile_size["x"])

                if cell.obstacle:
                    color = OBSTACLE_COLOR
                elif cell.unit:
                    color = UNIT_COLOR
                else:
                    color = GRID_COLOR

                pygame.draw.rect(self.screen, color, rect)
                if (x, y) == selected_pos:
                    pygame.draw.rect(self.screen, SELECTED_COLOR, rect, 2)  # highlight

                pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)  # grid border

        pygame.display.flip()
