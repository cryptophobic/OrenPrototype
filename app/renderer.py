from typing import Optional

import pygame

from app import config
from app.collections.actor_collection import ActorCollection
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

        x_offset = config.SCREEN_SIZE[0] // self.grid.width
        y_offset = config.SCREEN_SIZE[1] // self.grid.height

        tile_size = {
            "x": (config.SCREEN_SIZE[0] - (x_offset * 2)) // self.grid.width,
            "y": (config.SCREEN_SIZE[1] - (y_offset * 2)) // self.grid.height,
        }

        """Draw the grid and all objects"""
        self.screen.fill((0, 0, 0))

        collection = ActorCollection()
        
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(Vec2(x, y))

                x_scaled = (x * tile_size["x"]) + x_offset
                y_scaled = (y * tile_size["y"]) + y_offset

                rect = pygame.Rect(
                    x_scaled,
                    y_scaled,
                    tile_size["x"],
                    tile_size["y"]
                )
                
                # Draw grid cell
                pygame.draw.rect(self.screen, config.GRID_COLOR, rect)

                for item in cell.coordinate_holders:
                    collection.add(item)

                pygame.draw.rect(self.screen, config.BORDER_COLOR, rect, 1)  # grid border

        for item in collection:
            x = item.coordinates.x
            y = item.coordinates.y
            x_scaled = (x * tile_size["x"]) + (x_offset // 1)
            y_scaled = (y * tile_size["y"]) + (y_offset // 1)
            icon = item.shape.icon
            scaled_icon = pygame.transform.scale(icon, (tile_size["x"] * 1, tile_size["y"] * 1))
            self.screen.blit(scaled_icon, (x_scaled, y_scaled))

        pygame.display.flip()