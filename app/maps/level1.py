from app.config import NpcAnimations
from app.core.vectors import CustomVec2i
from app.engine.message_broker.types import Controls
from app.maps.level import LevelBuilder, map_dir
from app.objects.types import UnitStats
from app.registry.icon_registry import Icons


class Level1Builder(LevelBuilder):
    def __init__(self):
        super().__init__(
            name="level1",
            width=50,
            height=38,
            map_path=map_dir / "test_level" / "test.tmx"
        )

    def create_entities(self):
        # Create static objects from TMX layers
        self.create_static_objects_from_tmx_layer("Walls")
        # You can add more layers like:
        # self.create_static_objects_from_tmx_layer("Water", {tile_id: "water" for tile_id in water_tile_ids})
        
        # Create cursor
        cursor = self.create_cursor(CustomVec2i(4, 8))
        self.level.actors_collection.add(cursor)

        # Create player unit with animations
        player_animations = {
            NpcAnimations.ARMED_IDLE: NpcAnimations.ARMED_IDLE,
            NpcAnimations.ARMED_RUN: NpcAnimations.ARMED_RUN,
            NpcAnimations.ARMED_HURT: NpcAnimations.ARMED_HURT,
            NpcAnimations.ARMED_WALK: NpcAnimations.ARMED_WALK,
            NpcAnimations.ARMED_DEATH: NpcAnimations.ARMED_DEATH,
            NpcAnimations.ARMED_ATTACK: NpcAnimations.ARMED_ATTACK,
            NpcAnimations.ARMED_RUN_ATTACK: NpcAnimations.ARMED_RUN_ATTACK,
            NpcAnimations.ARMED_WALK_ATTACK: NpcAnimations.ARMED_WALK_ATTACK,
        }
        player_stats = UnitStats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        player = self.create_unit(
            position=CustomVec2i(31, 19),
            stats=player_stats,
            icon=Icons.PLAYER,
            animations=player_animations,
            name="Adventurer"
        )
        self.level.actors_collection.add(player)

        # Create enemy unit with animations
        enemy_animations = {
            NpcAnimations.ENEMY_IDLE: NpcAnimations.ENEMY_IDLE,
            NpcAnimations.ENEMY_RUN: NpcAnimations.ENEMY_RUN,
            NpcAnimations.ENEMY_HURT: NpcAnimations.ENEMY_HURT,
            NpcAnimations.ENEMY_WALK: NpcAnimations.ENEMY_WALK,
            NpcAnimations.ENEMY_DEATH: NpcAnimations.ENEMY_DEATH,
            NpcAnimations.ENEMY_ATTACK: NpcAnimations.ENEMY_ATTACK,
            NpcAnimations.ENEMY_RUN_ATTACK: NpcAnimations.ENEMY_RUN_ATTACK,
            NpcAnimations.ENEMY_WALK_ATTACK: NpcAnimations.ENEMY_WALK_ATTACK,
        }
        enemy_stats = UnitStats(STR=5, DEX=1, CON=5, INT=2, WIS=2, CHA=1, HP=10, initiative=1)
        enemy = self.create_unit(
            position=CustomVec2i(21, 18),
            stats=enemy_stats,
            icon=Icons.ENEMY,
            animations=enemy_animations,
            name="Enemy"
        )
        self.level.actors_collection.add(enemy)

        # Create puppeteer for player control
        puppeteer = self.create_puppeteer(player)
        self.level.actors_collection.add(puppeteer)

    def setup_controls(self) -> Controls:
        return self.create_standard_controls()

    def add_wall(self, position: CustomVec2i):
        """Add a wall to the level"""
        wall = self.create_wall(position)
        self.level.actors_collection.add(wall)
        self.level.grid.place(wall, wall.coordinates)
