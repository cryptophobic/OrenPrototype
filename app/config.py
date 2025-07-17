from dataclasses import dataclass
from enum import Enum, auto

from pyglet.image import Animation

FPS = 60
SCREEN_SIZE = (1300, 1100)

# Grid colors
GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (150, 150, 150)

Y_MODIFIER = -1

class NpcAnimations(Enum):
    ENEMY_ATTACK = auto()
    ENEMY_DEATH = auto()
    ENEMY_HURT = auto()
    ENEMY_IDLE = auto()
    ENEMY_RUN = auto()
    ENEMY_RUN_ATTACK = auto()
    ENEMY_WALK = auto()
    ENEMY_WALK_ATTACK = auto()

    ARMED_ATTACK = auto()
    ARMED_DEATH = auto()
    ARMED_HURT = auto()
    ARMED_IDLE = auto()
    ARMED_RUN = auto()
    ARMED_RUN_ATTACK = auto()
    ARMED_WALK = auto()
    ARMED_WALK_ATTACK = auto()

    DEATH = auto()
    HURT = auto()
    IDLE = auto()
    RUN = auto()
    WALK = auto()

@dataclass
class AnimationFileDetails:
    path: str
    sprite_width: int
    sprite_height: int
    frames: int

animation_paths: dict[NpcAnimations, AnimationFileDetails] = {
    NpcAnimations.ENEMY_ATTACK: AnimationFileDetails("goblin/Attack_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_DEATH: AnimationFileDetails("goblin/Death_full.png", 64, 64, 7),
    NpcAnimations.ENEMY_HURT: AnimationFileDetails("goblin/Hurt_full.png", 64, 64, 5),
    NpcAnimations.ENEMY_IDLE: AnimationFileDetails("goblin/Idle_full.png", 64, 64, 12),
    NpcAnimations.ENEMY_RUN: AnimationFileDetails("goblin/Run_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_RUN_ATTACK: AnimationFileDetails("goblin/Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_WALK: AnimationFileDetails("goblin/Walk_full.png", 64, 64, 6),
    NpcAnimations.ENEMY_WALK_ATTACK: AnimationFileDetails("goblin/Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.ARMED_ATTACK: AnimationFileDetails("male/Sword_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_DEATH: AnimationFileDetails("male/Sword_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_HURT: AnimationFileDetails("male/Sword_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_IDLE: AnimationFileDetails("male/Sword_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_RUN: AnimationFileDetails("male/Sword_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_RUN_ATTACK: AnimationFileDetails("male/Sword_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_WALK: AnimationFileDetails("male/Sword_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_WALK_ATTACK: AnimationFileDetails("male/Sword_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.DEATH: AnimationFileDetails("male/Unarmed_Death_full.png", 64, 64, 7),
    NpcAnimations.HURT: AnimationFileDetails("male/Unarmed_Hurt_full.png", 64, 64, 5),
    NpcAnimations.IDLE: AnimationFileDetails("male/Unarmed_Idle_full.png", 64, 64, 12),
    NpcAnimations.RUN: AnimationFileDetails("male/Unarmed_Run_full.png", 64, 64, 8),
    NpcAnimations.WALK: AnimationFileDetails("male/Unarmed_Walk_full.png", 64, 64, 6),
}

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
