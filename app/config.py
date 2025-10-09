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

@dataclass
class AnimationFileDetails:
    animation: UnitStates
    path: str
    sprite_width: int
    sprite_height: int
    frames: int
    front_offset: int = 0
    back_offset: int = 3
    left_offset: int = 1
    right_offset: int = 2

animation_paths: dict[NpcAnimations, AnimationFileDetails] = {
    NpcAnimations.ENEMY_ATTACK: AnimationFileDetails(
        animation=UnitStates.ATTACK,
        path="goblin/Attack_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=8,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_DEATH: AnimationFileDetails(
        animation=UnitStates.DEATH,
        path="goblin/Death_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=7,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_HURT: AnimationFileDetails(
        animation=UnitStates.HURT,
        path="goblin/Hurt_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=5,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_IDLE: AnimationFileDetails(
        animation=UnitStates.IDLE,
        path="goblin/Idle_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=4,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_RUN: AnimationFileDetails(
        animation=UnitStates.RUN,
        path="goblin/Run_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=8,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_RUN_ATTACK: AnimationFileDetails(
        animation=UnitStates.RUN_ATTACK,
        path="goblin/Run_Attack_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=8,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_WALK: AnimationFileDetails(
        animation=UnitStates.WALK,
        path="goblin/Walk_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=6,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),
    NpcAnimations.ENEMY_WALK_ATTACK: AnimationFileDetails(
        animation=UnitStates.WALK_ATTACK,
        path="goblin/Walk_Attack_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=6,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),

    NpcAnimations.ARMED_ATTACK: AnimationFileDetails(UnitStates.ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_DEATH: AnimationFileDetails(UnitStates.DEATH, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_HURT: AnimationFileDetails(UnitStates.HURT, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_IDLE: AnimationFileDetails(UnitStates.IDLE, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_RUN: AnimationFileDetails(UnitStates.RUN, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_RUN_ATTACK: AnimationFileDetails(UnitStates.RUN_ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_WALK: AnimationFileDetails(UnitStates.WALK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_WALK_ATTACK: AnimationFileDetails(UnitStates.WALK_ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.ARMED_NAKED_ATTACK: AnimationFileDetails(UnitStates.ATTACK, "male/Sword_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_DEATH: AnimationFileDetails(UnitStates.DEATH, "male/Sword_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_NAKED_HURT: AnimationFileDetails(UnitStates.HURT, "male/Sword_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_NAKED_IDLE: AnimationFileDetails(UnitStates.IDLE, "male/Sword_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_NAKED_RUN: AnimationFileDetails(UnitStates.RUN, "male/Sword_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_RUN_ATTACK: AnimationFileDetails(UnitStates.RUN_ATTACK, "male/Sword_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_WALK: AnimationFileDetails(UnitStates.WALK, "male/Sword_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_NAKED_WALK_ATTACK: AnimationFileDetails(UnitStates.WALK_ATTACK, "male/Sword_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.DEATH: AnimationFileDetails(UnitStates.DEATH, "male/Unarmed_Death_full.png", 64, 64, 7),
    NpcAnimations.HURT: AnimationFileDetails(UnitStates.HURT, "male/Unarmed_Hurt_full.png", 64, 64, 5),
    NpcAnimations.IDLE: AnimationFileDetails(UnitStates.IDLE, "male/Unarmed_Idle_full.png", 64, 64, 12),
    NpcAnimations.RUN: AnimationFileDetails(UnitStates.RUN, "male/Unarmed_Run_full.png", 64, 64, 8),
    NpcAnimations.WALK: AnimationFileDetails(UnitStates.WALK, "male/Unarmed_Walk_full.png", 64, 64, 6),
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
