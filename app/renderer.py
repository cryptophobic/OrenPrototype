from typing import Optional

import pygame

from app import config
from app.core.vectors import Vec2
from app.protocols.engine.grid.grid_protocol import GridProtocol


class Renderer:
    def __init__(self):
        pygame.init()
        self.grid: Optional[GridProtocol] = None
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("OrenPrototype - App Version")
        self.screen.fill((0, 0, 0))

    def draw(self):

        tile_size = {
            "x": config.SCREEN_SIZE[0] // self.grid.width,
            "y": config.SCREEN_SIZE[1] // self.grid.height,
        }

        """Draw the grid and all objects"""
        self.screen.fill((0, 0, 0))
        
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(Vec2(x, y))
                rect = pygame.Rect(
                    x * tile_size["x"],
                    y * tile_size["y"],
                    tile_size["x"],
                    tile_size["y"]
                )
                
                # Draw grid cell
                pygame.draw.rect(self.screen, config.GRID_COLOR, rect)

                for item in cell.coordinate_holders:
                    icon = item.shape.icon
                    scaled_icon = pygame.transform.scale(icon, (tile_size["x"], tile_size["y"]))
                    self.screen.blit(scaled_icon, (x * tile_size["x"], y * tile_size["y"]))

                pygame.draw.rect(self.screen, config.BORDER_COLOR, rect, 1)  # grid border

        pygame.display.flip()