from collections import defaultdict
from dataclasses import dataclass, field

import arcade
from typing import Dict, Set

from arcade import SpriteList
from pyglet.model.codecs.gltf import Texture

from app.behaviours.types import BufferedMoverState
from app.collections.coordinate_holder_collection import CoordinateHolderCollection
from app.config import Behaviours
from app.core.event_bus.consumer import Consumer
import app.core.event_bus.events as events
from app.core.types import NUM_LAYERS
from app.core.vectors import CustomVec2f, CustomVec2i
from app.engine.game_view.animated_sprite import AnimatedSprite
from app.objects.coordinate_holder import CoordinateHolder
from app.protocols.collections.actor_collection_protocol import ActorCollectionProtocol

@dataclass
class SpriteGameData:
    animation: list[Texture] = field(default_factory=list)
    coordinates: CustomVec2i = field(default_factory=CustomVec2i)
    moving_buffer: CustomVec2f = field(default_factory=CustomVec2f)


class SpriteRenderer(Consumer):
    def __init__(self, tile_size: int, get_tile_center_func):
        super().__init__()
        self.tile_size = tile_size
        self.get_tile_center = get_tile_center_func

        self._sprite_list: list[SpriteList] = [SpriteList(use_spatial_hash=True) for _ in range(NUM_LAYERS)]
        self._actor_name_sprite_map: Dict[str, arcade.Sprite] = {}

        self.actor_sprite_list = arcade.SpriteList()
        self.cursor_sprite_list = arcade.SpriteList()
        self.actor_sprite_map: Dict[str, arcade.Sprite] = {}
        self._animation_game_data: dict[str, SpriteGameData] = defaultdict(SpriteGameData)
        self.register_handler(events.Events.AnimationUpdate, self._on_animation_changed)
        self.register_handler(events.Events.MotionUpdate, self._on_move)
        self.register_handler(events.Events.RegisterObject, self._on_object_registered)
        self.register_handler(events.Events.UnregisterObject, self._on_object_unregistered)

    def _on_object_unregistered(self, payload: events.UnregisterObjectPayload):
        name = payload.object_name
        sprite = self._actor_name_sprite_map.pop(name, None)
        if not sprite:
            return

        sprite.remove_from_sprite_lists()
        self._animation_game_data.pop(name, None)

    def _on_object_registered(self, payload: events.RegisterObjectPayload):
        sprite = (
            AnimatedSprite(payload.animations, 0.5)
            if payload.object_type == events.ObjectTypes.ANIMATED
            else arcade.Sprite(payload.icon_path, scale=self.tile_size / 16)
        )
        self._sprite_list[payload.z_index].append(sprite)
        self._actor_name_sprite_map[payload.object_name] = sprite

    def _on_animation_changed(self, payload: events.AnimationUpdatePayload):
        self._animation_game_data[payload.actor_name].animation = payload.animation

    def _on_move(self, payload: events.MotionUpdatePayload):
        data = self._animation_game_data[payload.actor_name]
        data.coordinates = payload.coordinates
        data.moving_buffer = payload.moving_buffer

    def update_pending_sprites(self):
        pass

    def update_sprites(self, actor_collection: ActorCollectionProtocol) -> bool:
        current_actor_ids = set()
        changes_made = False
        
        for coordinate_holder in actor_collection.get_by_type(CoordinateHolder, CoordinateHolderCollection)\
                .filter(lambda a: a.shape is not None):
            current_actor_ids.add(coordinate_holder.id)
            changes_made |= self._update_actor_sprite(coordinate_holder)
            
        changes_made |= self._remove_obsolete_sprites(current_actor_ids)
        return changes_made
    
    def _update_actor_sprite(self, coordinate_holder: CoordinateHolder) -> bool:
        sprite_created = False
        
        if coordinate_holder.name not in self.actor_sprite_map:
            sprite = self._create_sprite_for_actor(coordinate_holder)
            self.actor_sprite_map[coordinate_holder.name] = sprite
            
            if coordinate_holder.name == "Cursor":
                self.cursor_sprite_list.append(sprite)
            else:
                self.actor_sprite_list.append(sprite)
            sprite_created = True
        else:
            sprite = self.actor_sprite_map[coordinate_holder.name]
            
        self._position_sprite(sprite, coordinate_holder)
        if isinstance(sprite, AnimatedSprite) and coordinate_holder.name in self._animation_pending_sprites:
            sprite.set_animation(coordinate_holder.shape.get_textures())
            self._animation_pending_sprites.remove(coordinate_holder.name)

        return sprite_created
    
    def _create_sprite_for_actor(self, coordinate_holder: CoordinateHolder) -> arcade.Sprite:
        if len(coordinate_holder.shape.animations) == 0:
            icon_path = coordinate_holder.shape.icon_path
            return arcade.Sprite(icon_path, scale=self.tile_size / 16)
        else:
            current_animation = coordinate_holder.shape.get_textures()
            return AnimatedSprite(current_animation, 0.5)
    
    def _position_sprite(self, sprite: arcade.Sprite, coordinate_holder: CoordinateHolder):
        x, y = coordinate_holder.coordinates.x, coordinate_holder.coordinates.y

        state = coordinate_holder.extract_behaviour_data(Behaviours.BUFFERED_MOVER)
        moving_buffer = state.moving_buffer if isinstance(state, BufferedMoverState) else CustomVec2f(0.0, 0.0)
        
        sprite.center_x = self.get_tile_center(x) + moving_buffer.x * self.tile_size
        sprite.center_y = self.get_tile_center(y) + moving_buffer.y * self.tile_size

    def _remove_obsolete_sprites(self, current_actor_ids: Set[str]) -> bool:
        to_remove = [actor_id for actor_id in self.actor_sprite_map if actor_id not in current_actor_ids]
        
        for actor_id in to_remove:
            sprite = self.actor_sprite_map.pop(actor_id)
            if sprite in self.actor_sprite_list:
                self.actor_sprite_list.remove(sprite)
            elif sprite in self.cursor_sprite_list:
                self.cursor_sprite_list.remove(sprite)
                
        return len(to_remove) > 0
    
    def draw(self):
        self.actor_sprite_list.draw()
        self.cursor_sprite_list.draw()
        
    def update(self):
        self.actor_sprite_list.update()