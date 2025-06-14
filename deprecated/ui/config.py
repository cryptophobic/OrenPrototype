# from application.game.Player import Player
# from application.game.controls import wasd, uldr, tfgh
from enum import Enum, auto

import pygame

FPS = 60
SCREEN_SIZE = (1000, 800)


players = [
    # Player(name='player1', controls=uldr, speed=0.5),
    # Player(name='player2', controls=wasd, speed=1.5),
    # Player(name='player3', controls=tfgh, speed=1)
]

class Behaviours(Enum):
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