from enum import Enum, auto

import pygame

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


controls_presets = {
    Behaviours.MOVEABLE: {
        pygame.K_UP: 'move_up',
        pygame.K_DOWN: 'move_down',
        pygame.K_LEFT: 'move_left',
        pygame.K_RIGHT: 'move_right',
    },
    Behaviours.AGGRESSIVE: {
        pygame.K_a: 'attack',
        pygame.K_s: 'defense',
        pygame.K_d: 'dodge',
        pygame.K_e: 'end_turn',
    },
    Behaviours.FRIGHTENED: {
        pygame.K_e: 'end_turn',
    }
}

controls_presets[Behaviours.CURSOR] = {
    **controls_presets[Behaviours.MOVEABLE],
    pygame.K_KP_ENTER: 'select',
    pygame.K_ESCAPE: 'deselect'
}