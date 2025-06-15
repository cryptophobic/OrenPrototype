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

    GENERAL = auto()

    # Can be possessed. Used by player and NPCs
    MOVEABLE = auto()
    AGGRESSIVE = auto()
    FRIGHTENED = auto()

    # Cannot be possessed. Used by NPCs
    ENEMY = auto()
    FRIEND = auto()
    NEUTRAL = auto()

    # For cursor
    WATCHER = auto()


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

controls_presets[Behaviours.WATCHER] = {
    **controls_presets[Behaviours.MOVEABLE],
    pygame.K_KP_ENTER: 'select',
    pygame.K_ESCAPE: 'deselect'
}