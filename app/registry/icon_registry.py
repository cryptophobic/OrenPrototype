from pathlib import Path
from typing import Dict

from enum import Enum

class Icons(str, Enum):
    CURSOR = "icons/cursor.png"
    ENEMY = "icons/enemy.png"
    PLAYER = "icons/player.png"
    WALLS = "icons/walls.png"

icons_storage_path: Dict[Icons, Path] = {}

def get_icon_path(name: Icons):
    if name not in icons_storage_path:
        current_path = Path(__file__).parent
        icon_path = current_path / name.value
        icons_storage_path[name] = icon_path

    return icons_storage_path[name]
