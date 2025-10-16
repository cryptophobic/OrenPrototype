from dataclasses import dataclass
from enum import Enum, auto

FPS = 60
SCREEN_SIZE = (1440, 1000)
TILE_SIZE = 16

# Grid colors
GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (150, 150, 150)

Y_MODIFIER = -1

class UnitStates(Enum):
    ATTACK = auto()
    DEATH = auto()
    HURT = auto()
    IDLE = auto()
    RUN = auto()
    RUN_ATTACK = auto()
    WALK = auto()
    WALK_ATTACK = auto()

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

    ARMED_NAKED_ATTACK = auto()
    ARMED_NAKED_DEATH = auto()
    ARMED_NAKED_HURT = auto()
    ARMED_NAKED_IDLE = auto()
    ARMED_NAKED_RUN = auto()
    ARMED_NAKED_RUN_ATTACK = auto()
    ARMED_NAKED_WALK = auto()
    ARMED_NAKED_WALK_ATTACK = auto()

    UNARMED_NAKED_DEATH = auto()
    UNARMED_NAKED_HURT = auto()
    UNARMED_NAKED_IDLE = auto()
    UNARMED_NAKED_RUN = auto()
    UNARMED_NAKED_WALK = auto()


@dataclass
class AnimationFileDetails:
    path: str
    sprite_width: int
    sprite_height: int
    frames: int
    front_offset: int = 0
    back_offset: int = 3
    left_offset: int = 1
    right_offset: int = 2

animation_paths: dict[NpcAnimations, AnimationFileDetails] = {
    NpcAnimations.ENEMY_ATTACK: AnimationFileDetails("goblin/Attack_full.png", 64, 64, 8, 0, 1, 2, 3),
    NpcAnimations.ENEMY_DEATH: AnimationFileDetails("goblin/Death_full.png", 64, 64, 7, 0, 1, 2, 3),
    NpcAnimations.ENEMY_HURT: AnimationFileDetails("goblin/Hurt_full.png", 64, 64, 5, 0, 1, 2, 3),
    NpcAnimations.ENEMY_IDLE: AnimationFileDetails("goblin/Idle_full.png", 64, 64, 4, 0, 1, 2, 3),
    NpcAnimations.ENEMY_RUN: AnimationFileDetails("goblin/Run_full.png", 64, 64, 8, 0, 1, 2, 3),
    NpcAnimations.ENEMY_RUN_ATTACK: AnimationFileDetails("goblin/Run_Attack_full.png", 64, 64, 8, 0, 1, 2, 3),
    NpcAnimations.ENEMY_WALK: AnimationFileDetails("goblin/Walk_full.png", 64, 64, 6, 0, 1, 2, 3),
    NpcAnimations.ENEMY_WALK_ATTACK: AnimationFileDetails("goblin/Walk_Attack_full.png", 64, 64, 6, 0, 1, 2, 3),

    NpcAnimations.ARMED_ATTACK: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_DEATH: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_HURT: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_IDLE: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_RUN: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_RUN_ATTACK: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_WALK: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_WALK_ATTACK: AnimationFileDetails("swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.ARMED_NAKED_ATTACK: AnimationFileDetails("male/Sword_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_DEATH: AnimationFileDetails("male/Sword_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_NAKED_HURT: AnimationFileDetails("male/Sword_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_NAKED_IDLE: AnimationFileDetails("male/Sword_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_NAKED_RUN: AnimationFileDetails("male/Sword_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_RUN_ATTACK: AnimationFileDetails("male/Sword_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_WALK: AnimationFileDetails("male/Sword_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_NAKED_WALK_ATTACK: AnimationFileDetails("male/Sword_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.UNARMED_NAKED_DEATH: AnimationFileDetails("male/Unarmed_Death_full.png", 64, 64, 7),
    NpcAnimations.UNARMED_NAKED_HURT: AnimationFileDetails("male/Unarmed_Hurt_full.png", 64, 64, 5),
    NpcAnimations.UNARMED_NAKED_IDLE: AnimationFileDetails("male/Unarmed_Idle_full.png", 64, 64, 12),
    NpcAnimations.UNARMED_NAKED_RUN: AnimationFileDetails("male/Unarmed_Run_full.png", 64, 64, 8),
    NpcAnimations.UNARMED_NAKED_WALK: AnimationFileDetails("male/Unarmed_Walk_full.png", 64, 64, 6),
}

class Behaviours(Enum):

    # Base class. Actor and descendants
    BEHAVIOUR = ".behaviour.Behaviour"

    # Orchestrator
    ANIMATED = ".animate.animated.Animated"

    # Puppeteer
    POSSESSOR = ".puppeteer.possessor.Possessor"

    # Unit
    VULNERABLE = ".units.vulnerable.Vulnerable"
    AGGRESSIVE = ".units.aggressive.Aggressive"
    FRIGHTENED = ".units.frightened.Frightened"
    ENEMY = ".units.enemy.Enemy"
    FRIEND = ".units.friend.Friend"
    NEUTRAL = ".units.neutral.Neutral"

    # CoordinateHolder and descendants
    DISCRETE_MOVER = ".moveable.discrete_mover.DiscreteMover"
    BUFFERED_MOVER = ".moveable.buffered_mover.BufferedMover"
    CURSOR = ".moveable.cursor.Cursor"

    # StaticObject
    DESTRUCTIBLE = ".static_objects.destructible.Destructible"
    TRANSPORTABLE = ".static_objects.transportable.Transportable"
