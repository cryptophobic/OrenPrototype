from dataclasses import dataclass


@dataclass
class UnitStats:
    STR: int = 0
    DEX: int = 0
    CON: int = 0
    INT: int = 0
    WIS: int = 0
    CHA: int = 0
    HP: int = 0
    speed: float = 1 / 0.2
    initiative: int = 0
