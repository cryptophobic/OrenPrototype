from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntFlag, auto

import arcade

from pyglet.model.codecs.gltf import Texture

from app.core.event_bus.consumer import Consumer
import app.core.event_bus.events as events
import app.core.event_bus.types as event_types

from app.core.types import NUM_LAYERS
from app.core.vectors import CustomVec2f, CustomVec2i
from app.engine.game_view.animated_sprite import AnimatedSprite

@dataclass
class SpriteGameData:
    animation: list[Texture] = field(default_factory=list)
    coordinates: CustomVec2i = field(default_factory=CustomVec2i)
    moving_buffer: CustomVec2f = field(default_factory=CustomVec2f)

class Dirty(IntFlag):
    NONE = 0
    POS  = auto()
    ANIM = auto()

class SpriteRenderer(Consumer):
    def __init__(self, tile_size: int, get_tile_center_func):
        super().__init__()
        self.tile_size = tile_size
        self.get_tile_center = get_tile_center_func

        self._sprite_list: list[arcade.SpriteList] = [arcade.SpriteList(use_spatial_hash=True) for _ in range(NUM_LAYERS)]
        self._object_name_sprite_map: dict[str, arcade.Sprite] = {}

        self._animation_game_data: dict[str, SpriteGameData] = defaultdict(SpriteGameData)
        self._dirty: dict[str, Dirty] = {}

        self.register_handler(events.Events.AnimationUpdate, self._on_animation_changed)
        self.register_handler(events.Events.MotionUpdate, self._on_move)
        self.register_handler(events.Events.RegisterObject, self._on_object_registered)
        self.register_handler(events.Events.UnregisterObject, self._on_object_unregistered)

    def _mark(self, name: str, bits: Dirty):
        self._dirty[name] = self._dirty.get(name, Dirty.NONE) | bits

    def _on_object_unregistered(self, payload: event_types.UnregisterObjectPayload):
        name = payload.object_name
        sprite = self._object_name_sprite_map.pop(name, None)
        if not sprite:
            return

        sprite.remove_from_sprite_lists()
        self._animation_game_data.pop(name, None)
        self._dirty.pop(name, None)

    def _on_object_registered(self, payload: event_types.RegisterObjectPayload):
        sprite = (
            AnimatedSprite(payload.animations, 0.5)
            if payload.object_type == event_types.ObjectTypes.ANIMATED
            else arcade.Sprite(payload.icon_path, scale=self.tile_size / 16)
        )
        self._sprite_list[payload.z_index].append(sprite)
        self._object_name_sprite_map[payload.object_name] = sprite
        self._animation_game_data[payload.object_name].coordinates = payload.coordinates
        self._mark(payload.object_name, Dirty.POS)

    def _on_animation_changed(self, payload: event_types.AnimationUpdatePayload):
        self._animation_game_data[payload.object_name].animation = payload.animation
        self._mark(payload.object_name, Dirty.ANIM)

    def _on_move(self, payload: event_types.MotionUpdatePayload):
        data = self._animation_game_data[payload.object_name]
        data.coordinates = payload.coordinates
        data.moving_buffer = payload.moving_buffer
        self._mark(payload.object_name, Dirty.POS)

    def update_sprites(self, eps: float = 1e-9) -> bool:
        if not self._dirty:
            return False

        dirty_now = self._dirty
        self._dirty = {}

        for name, bits in dirty_now.items():
            sprite = self._object_name_sprite_map.get(name)
            if not sprite:
                continue
            data = self._animation_game_data.get(name)
            if not data:
                continue

            if (bits & Dirty.ANIM) and isinstance(sprite, AnimatedSprite) and sprite.textures is not data.animation:
                sprite.set_animation(data.animation)

            if bits & Dirty.POS:
                # only write centers when they actually differ (avoids GPU churn)
                x, y = data.coordinates.x, data.coordinates.y
                mbx, mby = data.moving_buffer.x, data.moving_buffer.y
                cx = self.get_tile_center(x) + mbx * self.tile_size
                cy = self.get_tile_center(y) + mby * self.tile_size
                if abs(sprite.center_x - cx) > eps:
                    sprite.center_x = cx
                if abs(sprite.center_y - cy) > eps:
                    sprite.center_y = cy

        return True

    def draw(self):
        for sprite_list in self._sprite_list:
            sprite_list.draw()

    def update(self):
        for sprite_list in self._sprite_list:
            sprite_list.update()
