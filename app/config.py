from dataclasses import dataclass
from enum import Enum, auto

FPS = 60
SCREEN_SIZE = (1440, 1000)

# Grid colors
GRID_COLOR = (200, 200, 200)
OBSTACLE_COLOR = (100, 100, 100)
SELECTED_COLOR = (255, 255, 0)
UNIT_COLOR = (0, 128, 255)
BORDER_COLOR = (150, 150, 150)

Y_MODIFIER = -1

class CommonAnimations(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()
    HURT = auto()
    DEATH = auto()
    RUN = auto()
    RUN_ATTACK = auto()
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

    DEATH = auto()
    HURT = auto()
    IDLE = auto()
    RUN = auto()
    WALK = auto()

@dataclass
class AnimationFileDetails:
    animation: CommonAnimations
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
        animation=CommonAnimations.ATTACK,
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
        animation=CommonAnimations.DEATH,
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
        animation=CommonAnimations.HURT,
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
        animation=CommonAnimations.IDLE,
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
        animation=CommonAnimations.RUN,
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
        animation=CommonAnimations.RUN_ATTACK,
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
        animation=CommonAnimations.WALK,
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
        animation=CommonAnimations.WALK_ATTACK,
        path="goblin/Walk_Attack_full.png",
        sprite_width=64,
        sprite_height=64,
        frames=6,
        front_offset=0,
        back_offset=1,
        left_offset=2,
        right_offset=3,
    ),

    NpcAnimations.ARMED_ATTACK: AnimationFileDetails(CommonAnimations.ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_DEATH: AnimationFileDetails(CommonAnimations.DEATH, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_HURT: AnimationFileDetails(CommonAnimations.HURT, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_IDLE: AnimationFileDetails(CommonAnimations.IDLE, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_RUN: AnimationFileDetails(CommonAnimations.RUN, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_RUN_ATTACK: AnimationFileDetails(CommonAnimations.RUN_ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_WALK: AnimationFileDetails(CommonAnimations.WALK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_WALK_ATTACK: AnimationFileDetails(CommonAnimations.WALK_ATTACK, "swordsman/Swordsman_lvl3/Swordsman_lvl3_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.ARMED_NAKED_ATTACK: AnimationFileDetails(CommonAnimations.ATTACK, "male/Sword_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_DEATH: AnimationFileDetails(CommonAnimations.DEATH, "male/Sword_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_NAKED_HURT: AnimationFileDetails(CommonAnimations.HURT, "male/Sword_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_NAKED_IDLE: AnimationFileDetails(CommonAnimations.IDLE, "male/Sword_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_NAKED_RUN: AnimationFileDetails(CommonAnimations.RUN, "male/Sword_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_RUN_ATTACK: AnimationFileDetails(CommonAnimations.RUN_ATTACK, "male/Sword_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_NAKED_WALK: AnimationFileDetails(CommonAnimations.WALK, "male/Sword_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_NAKED_WALK_ATTACK: AnimationFileDetails(CommonAnimations.WALK_ATTACK, "male/Sword_Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.DEATH: AnimationFileDetails(CommonAnimations.DEATH, "male/Unarmed_Death_full.png", 64, 64, 7),
    NpcAnimations.HURT: AnimationFileDetails(CommonAnimations.HURT, "male/Unarmed_Hurt_full.png", 64, 64, 5),
    NpcAnimations.IDLE: AnimationFileDetails(CommonAnimations.IDLE, "male/Unarmed_Idle_full.png", 64, 64, 12),
    NpcAnimations.RUN: AnimationFileDetails(CommonAnimations.RUN, "male/Unarmed_Run_full.png", 64, 64, 8),
    NpcAnimations.WALK: AnimationFileDetails(CommonAnimations.WALK, "male/Unarmed_Walk_full.png", 64, 64, 6),
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
