from pathlib import Path

from app.core.animations import ArmedAnimations


class Shape:
    def __init__(self, icon_path: Path, animations: dict[ArmedAnimations, list[Path]] = None):
        self.icon_path: Path = icon_path
        self.animations: dict[ArmedAnimations, list[Path]] = animations or {}
        self.current_animation: ArmedAnimations = ArmedAnimations.IDLE
        pass
