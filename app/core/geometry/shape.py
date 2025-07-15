from pathlib import Path


class Shape:
    def __init__(self, icon_path: Path, animations: dict[str, list[Path]] = None):
        self.icon_path: Path = icon_path
        self.animations: dict[str, list[Path]] = animations or {}
        pass
