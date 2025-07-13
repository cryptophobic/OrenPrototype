from enum import Enum

FPS = 60
SCREEN_SIZE = (1000, 800)

# Grid colors
GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (50, 50, 50)


class Behaviours(Enum):

    # Base class. Actor and descendants
    BEHAVIOUR = ".behaviour.Behaviour"

    # Orchestrator
    INPUT_HANDLER = ".orchestrator.input_handler.InputHandler"

    # Puppeteer
    POSSESSOR = ".puppeteer.possessor.Possessor"

    # Unit
    VULNERABLE = ".units.vulnerable.Vulnerable"
    AGGRESSIVE = ".units.aggressive.Aggressive"
    FRIGHTENED = ".units.frightened.Frightened"
    ENEMY = ".units.frightened.Frightened"
    FRIEND = ".units.friend.friend"
    NEUTRAL = ".units.neutral.neutral"

    # CoordinateHolder and descendants
    MOVEABLE = ".coordinate_holder.moveable.Moveable"

    # StaticObject
    DESTRUCTIBLE = ".static_objects.destructible.Destructible"
    TRANSPORTABLE = ".static_objects.transportable.Transportable"
