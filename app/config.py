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

animation_paths: dict[NpcAnimations, AnimationFileDetails] = {
    NpcAnimations.ENEMY_ATTACK: AnimationFileDetails(CommonAnimations.ATTACK, "goblin/Attack_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_DEATH: AnimationFileDetails(CommonAnimations.DEATH, "goblin/Death_full.png", 64, 64, 7),
    NpcAnimations.ENEMY_HURT: AnimationFileDetails(CommonAnimations.HURT, "goblin/Hurt_full.png", 64, 64, 5),
    NpcAnimations.ENEMY_IDLE: AnimationFileDetails(CommonAnimations.IDLE, "goblin/Idle_full.png", 64, 64, 4),
    NpcAnimations.ENEMY_RUN: AnimationFileDetails(CommonAnimations.RUN, "goblin/Run_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_RUN_ATTACK: AnimationFileDetails(CommonAnimations.RUN_ATTACK, "goblin/Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ENEMY_WALK: AnimationFileDetails(CommonAnimations.WALK, "goblin/Walk_full.png", 64, 64, 6),
    NpcAnimations.ENEMY_WALK_ATTACK: AnimationFileDetails(CommonAnimations.WALK_ATTACK, "goblin/Walk_Attack_full.png", 64, 64, 6),

    NpcAnimations.ARMED_ATTACK: AnimationFileDetails(CommonAnimations.ATTACK, "male/Sword_attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_DEATH: AnimationFileDetails(CommonAnimations.DEATH, "male/Sword_Death_full.png", 64, 64, 7),
    NpcAnimations.ARMED_HURT: AnimationFileDetails(CommonAnimations.HURT, "male/Sword_Hurt_full.png", 64, 64, 5),
    NpcAnimations.ARMED_IDLE: AnimationFileDetails(CommonAnimations.IDLE, "male/Sword_Idle_full.png", 64, 64, 12),
    NpcAnimations.ARMED_RUN: AnimationFileDetails(CommonAnimations.RUN, "male/Sword_Run_full.png", 64, 64, 8),
    NpcAnimations.ARMED_RUN_ATTACK: AnimationFileDetails(CommonAnimations.RUN_ATTACK, "male/Sword_Run_Attack_full.png", 64, 64, 8),
    NpcAnimations.ARMED_WALK: AnimationFileDetails(CommonAnimations.WALK, "male/Sword_Walk_full.png", 64, 64, 6),
    NpcAnimations.ARMED_WALK_ATTACK: AnimationFileDetails(CommonAnimations.WALK_ATTACK, "male/Sword_Walk_Attack_full.png", 64, 64, 6),

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
