from pathlib import Path
from typing import Dict

import pygame

from enum import Enum

class Icons(str, Enum):
    CURSOR = "icons/cursor.png"
    ENEMY = "icons/enemy.png"
    PLAYER = "icons/player.png"
    WALLS = "icons/walls.png"

icons_storage: Dict[Icons, pygame.Surface] = {}

def get_icon(name: Icons):
    if name not in icons_storage:
        current_path = Path(__file__).parent
        icon_path = current_path / name.value

        icons_storage[name] = pygame.image.load(icon_path).convert_alpha()
        # TODO: pygame.transform.scale(pygame.image.load(icon_path).convert_alpha(), width_of_cell, height_of_cell)

    return icons_storage[name]
