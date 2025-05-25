from ui.actors.shape import Shape as BaseShape
from pathlib import Path
import pygame


class Shape(BaseShape):
    def __init__(self):
        super().__init__()
        root = Path(__file__).parents[3]
        icon_path = root / "resources" / "icons" / "cursor.png"

        self.icon = pygame.image.load(icon_path).convert_alpha()

