import pygame
from app.engine.state.grid import Grid
from app import config
from app.helpers.vectors import Vec2


class Renderer:
    def __init__(self, grid: Grid):
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("OrenPrototype - App Version")
        self.grid = grid
        self.tile_size = {
            "x": config.SCREEN_SIZE[0] // grid.width,
            "y": config.SCREEN_SIZE[1] // grid.height,
        }
        self.screen.fill((0, 0, 0))

    def draw(self):
        """Draw the grid and all objects"""
        self.screen.fill((0, 0, 0))
        
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(Vec2(x, y))
                rect = pygame.Rect(
                    x * self.tile_size["x"], 
                    y * self.tile_size["y"], 
                    self.tile_size["x"], 
                    self.tile_size["y"]
                )
                
                # Draw grid cell
                pygame.draw.rect(self.screen, config.GRID_COLOR, rect)

                # Draw occupants (if any)
                if cell.is_occupied():
                    # For now, just draw a colored rectangle for occupants
                    pygame.draw.rect(self.screen, config.UNIT_COLOR, rect)

                # Draw selection highlight
                if cell.selected:
                    pygame.draw.rect(self.screen, config.SELECTED_COLOR, rect, 2)

                # Draw grid border
                pygame.draw.rect(self.screen, config.BORDER_COLOR, rect, 1)

        pygame.display.flip()