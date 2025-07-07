import pygame

from app.context.context import Context
from app import config
from app.helpers.vectors import Vec2


class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("OrenPrototype - App Version")
        self.screen.fill((0, 0, 0))

    def draw(self):

        grid = Context.instance().grid_context.grid
        tile_size = {
            "x": config.SCREEN_SIZE[0] // grid.width,
            "y": config.SCREEN_SIZE[1] // grid.height,
        }

        """Draw the grid and all objects"""
        self.screen.fill((0, 0, 0))
        
        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(Vec2(x, y))
                rect = pygame.Rect(
                    x * tile_size["x"],
                    y * tile_size["y"],
                    tile_size["x"],
                    tile_size["y"]
                )
                
                # Draw grid cell
                pygame.draw.rect(self.screen, config.GRID_COLOR, rect)

                for item in list(cell.static_objects.values()) + list(cell.coordinate_holders.values()):
                    icon = item.shape.icon
                    scaled_icon = pygame.transform.scale(icon, (tile_size["x"], tile_size["y"]))
                    self.screen.blit(scaled_icon, (x * tile_size["x"], y * tile_size["y"]))

                pygame.draw.rect(self.screen, config.BORDER_COLOR, rect, 1)  # grid border

        pygame.display.flip()