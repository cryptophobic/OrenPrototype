from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

import arcade

from app.core.debug import Debug
from app.engine.game_view.animated_sprite import AnimatedSprite


class TMXAnimationParser:
    """Parses TMX files to extract tile animation data"""

    def __init__(self, tmx_file_path: str):
        self.tmx_path = Path(tmx_file_path)
        self.animations: Dict[int, List[Tuple[int, int]]] = {}  # tile_id -> [(frame_tileid, duration), ...]
        self.tilesets: Dict[str, Dict] = {}  # tileset_name -> tileset_info
        self.map_layers: Dict[str, List[List[int]]] = {}  # layer_name -> 2D grid of tile IDs
        self.map_width = 0
        self.map_height = 0
        self.tile_width = 0
        self.tile_height = 0
        self._parse_tmx()

    def _parse_tmx(self):
        """Parse the TMX file to extract animation and tileset information"""
        tree = ET.parse(self.tmx_path)
        root = tree.getroot()

        # Get map dimensions
        self.map_width = int(root.get('width'))
        self.map_height = int(root.get('height'))
        self.tile_width = int(root.get('tilewidth'))
        self.tile_height = int(root.get('tileheight'))

        # Parse tilesets
        for tileset in root.findall('tileset'):
            firstgid = int(tileset.get('firstgid'))

            # Check if this is an external tileset reference (TSX file)
            if tileset.get('source'):
                tsx_source = tileset.get('source')
                Debug.log(f"Found external tileset reference: {tsx_source} (firstgid: {firstgid})", __file__)
                self._parse_external_tileset(tsx_source, firstgid)
                continue

            # Handle inline tileset
            tileset_info = {
                'firstgid': firstgid,
                'name': tileset.get('name'),
                'tilewidth': int(tileset.get('tilewidth')),
                'tileheight': int(tileset.get('tileheight')),
                'tilecount': int(tileset.get('tilecount')),
                'columns': int(tileset.get('columns'))
            }

            # Get image source
            image_elem = tileset.find('image')
            if image_elem is not None:
                tileset_info['image_source'] = image_elem.get('source')
                tileset_info['image_width'] = int(image_elem.get('width'))
                tileset_info['image_height'] = int(image_elem.get('height'))

            self.tilesets[tileset_info['name']] = tileset_info

            # Parse animations within this tileset
            for tile in tileset.findall('tile'):
                tile_id = int(tile.get('id'))
                global_tile_id = tile_id + tileset_info['firstgid']

                animation_elem = tile.find('animation')
                if animation_elem is not None:
                    frames = []
                    for frame in animation_elem.findall('frame'):
                        frame_tileid = int(frame.get('tileid'))
                        duration = int(frame.get('duration'))
                        global_frame_id = frame_tileid + tileset_info['firstgid']
                        frames.append((global_frame_id, duration))

                    self.animations[global_tile_id] = frames
                    Debug.log(f"Found animation for tile {global_tile_id}: {len(frames)} frames", __file__)

        # Parse layers to find where tiles are placed
        for layer in root.findall('layer'):
            layer_name = layer.get('name')

            # Get the data element and parse CSV
            data_elem = layer.find('data')
            if data_elem is not None and data_elem.get('encoding') == 'csv':
                csv_data = data_elem.text.strip()
                # Parse CSV into 2D grid
                rows = []
                for line in csv_data.split('\n'):
                    if line.strip():
                        row = [int(x.strip()) for x in line.split(',') if x.strip()]
                        if row:  # Only add non-empty rows
                            rows.append(row)

                self.map_layers[layer_name] = rows
                Debug.log(f"Parsed layer '{layer_name}': {len(rows)} rows, {len(rows[0]) if rows else 0} columns", __file__)

    def _parse_external_tileset(self, tsx_source: str, firstgid: int):
        """Parse an external TSX tileset file"""
        # Build path to TSX file (relative to TMX file)
        tsx_path = self.tmx_path.parent / tsx_source

        if not tsx_path.exists():
            Debug.log(f"Warning: External tileset not found: {tsx_path}", __file__)
            return

        Debug.log(f"Parsing external tileset: {tsx_path}", __file__)

        # Parse the TSX file
        tsx_tree = ET.parse(tsx_path)
        tsx_root = tsx_tree.getroot()

        # Extract tileset info
        tileset_info = {
            'firstgid': firstgid,
            'name': tsx_root.get('name'),
            'tilewidth': int(tsx_root.get('tilewidth')),
            'tileheight': int(tsx_root.get('tileheight')),
            'tilecount': int(tsx_root.get('tilecount')),
            'columns': int(tsx_root.get('columns'))
        }

        # Get image source
        image_elem = tsx_root.find('image')
        if image_elem is not None:
            # Image path in TSX is relative to the TSX file location
            tsx_image_source = image_elem.get('source')
            # Build full path relative to TMX file (where TSX is located)
            tileset_info['image_source'] = tsx_image_source
            tileset_info['image_width'] = int(image_elem.get('width'))
            tileset_info['image_height'] = int(image_elem.get('height'))

        self.tilesets[tileset_info['name']] = tileset_info

        # Parse animations within this external tileset
        for tile in tsx_root.findall('tile'):
            tile_id = int(tile.get('id'))
            global_tile_id = tile_id + firstgid

            animation_elem = tile.find('animation')
            if animation_elem is not None:
                frames = []
                for frame in animation_elem.findall('frame'):
                    frame_tileid = int(frame.get('tileid'))
                    duration = int(frame.get('duration'))
                    global_frame_id = frame_tileid + firstgid
                    frames.append((global_frame_id, duration))

                self.animations[global_tile_id] = frames
                Debug.log(f"Found animation for tile {global_tile_id}: {len(frames)} frames", __file__)

    def get_animations(self) -> Dict[int, List[Tuple[int, int]]]:
        """Get all parsed animations"""
        return self.animations

    def get_tilesets(self) -> Dict[str, Dict]:
        """Get all parsed tilesets"""
        return self.tilesets

    def load_tileset_textures(self) -> Dict[int, arcade.Texture]:
        """Load all textures from tilesets and return a mapping of tile_id -> texture"""
        textures = {}

        for tileset_name, tileset_info in self.tilesets.items():
            if 'image_source' not in tileset_info:
                continue

            # Build path to tileset image
            # For external tilesets, image is relative to the TSX file location
            # For inline tilesets, image is relative to the TMX file location
            image_path = self.tmx_path.parent / tileset_info['image_source']

            if not image_path.exists():
                Debug.log(f"Warning: Tileset image not found: {image_path}", __file__)
                continue

            Debug.log(f"Loading tileset '{tileset_name}' from {image_path}", __file__)

            # Load the tileset image
            tileset_texture = arcade.load_texture(str(image_path))

            # Extract individual tile textures
            tile_width = tileset_info['tilewidth']
            tile_height = tileset_info['tileheight']
            columns = tileset_info['columns']
            tile_count = tileset_info['tilecount']
            firstgid = tileset_info['firstgid']

            for tile_index in range(tile_count):
                # Calculate tile position in the tileset
                col = tile_index % columns
                row = tile_index // columns
                x = col * tile_width
                y = row * tile_height

                # Extract tile texture
                global_tile_id = tile_index + firstgid
                try:
                    tile_texture = tileset_texture.crop(x, y, tile_width, tile_height)
                    textures[global_tile_id] = tile_texture
                except Exception as e:
                    Debug.log(f"Error loading tile {global_tile_id}: {e}", __file__)

            Debug.log(f"  Loaded {tile_count} tiles from {tileset_name}", __file__)

        return textures

    def find_animated_tile_positions(self) -> List[Tuple[int, int, int]]:
        """Find positions of animated tiles in the map layers.
        Returns list of (tile_id, x, y) tuples for animated tiles."""
        positions = []

        for layer_name, layer_data in self.map_layers.items():
            for y, row in enumerate(layer_data):
                for x, tile_id in enumerate(row):
                    if tile_id in self.animations:
                        positions.append((tile_id, x, y))
                        Debug.log(f"Found animated tile {tile_id} at ({x}, {y}) in layer '{layer_name}'", __file__)

        return positions

    def find_animated_tile_positions_by_layer(self) -> Dict[str, List[Tuple[int, int, int]]]:
        """Find positions of animated tiles grouped by layer.
        Returns dict of layer_name -> list of (tile_id, x, y) tuples."""
        positions_by_layer = {}

        for layer_name, layer_data in self.map_layers.items():
            layer_positions = []
            for y, row in enumerate(layer_data):
                for x, tile_id in enumerate(row):
                    if tile_id in self.animations:
                        layer_positions.append((tile_id, x, y))
                        Debug.log(f"Found animated tile {tile_id} at ({x}, {y}) in layer '{layer_name}'", __file__)

            if layer_positions:
                positions_by_layer[layer_name] = layer_positions

        return positions_by_layer

    def create_animated_sprites(self, scaling: float = 1.0) -> Dict[int, AnimatedSprite]:
        """Create AnimatedTile sprites for all animations"""
        textures = self.load_tileset_textures()
        animated_sprites = {}

        for tile_id, frames in self.animations.items():
            # Get textures for animation frames
            frame_textures = []
            frame_durations = []

            for frame_tile_id, duration in frames:
                if frame_tile_id in textures:
                    texture = textures[frame_tile_id]
                    # Note: We'll handle scaling at the sprite level instead of texture level
                    # since arcade doesn't have easy texture scaling methods
                    frame_textures.append(texture)
                    frame_durations.append(duration)
                else:
                    Debug.log(f"Warning: Frame texture {frame_tile_id} not found for animation {tile_id}", __file__)

            if frame_textures:
                animated_sprite = AnimatedSprite(frame_textures, 1.0, frame_durations)
                # Apply scaling to the sprite
                if scaling != 1.0:
                    animated_sprite.scale = scaling
                animated_sprites[tile_id] = animated_sprite
                Debug.log(f"Created animated sprite for tile {tile_id} with {len(frame_textures)} frames", __file__)

        return animated_sprites

    def print_animation_info(self):
        """Print information about found animations"""
        Debug.log(f"\n=== TMX Animation Info ===", __file__)
        Debug.log(f"File: {self.tmx_path}", __file__)
        Debug.log(f"Found {len(self.animations)} animated tiles", __file__)
        Debug.log(f"Found {len(self.tilesets)} tilesets", __file__)

        for tileset_name, info in self.tilesets.items():
            Debug.log(f"\nTileset '{tileset_name}':", __file__)
            Debug.log(f"  - First GID: {info['firstgid']}", __file__)
            Debug.log(f"  - Tile size: {info['tilewidth']}x{info['tileheight']}", __file__)
            Debug.log(f"  - Tile count: {info['tilecount']}", __file__)
            if 'image_source' in info:
                Debug.log(f"  - Image: {info['image_source']}", __file__)

        Debug.log(f"\nAnimations:", __file__)
        for tile_id, frames in self.animations.items():
            Debug.log(f"  Tile {tile_id}: {len(frames)} frames", __file__)
            for i, (frame_id, duration) in enumerate(frames):
                Debug.log(f"    Frame {i}: tile {frame_id}, duration {duration}ms", __file__)


def load_animated_tilemap_from_parser(animation_parser: TMXAnimationParser, scaling: float = 1.0, layer_options: Dict = None):
    """
    Factory function to load a TMX tilemap with animated tiles from an existing parser.

    Args:
        animation_parser: Pre-existing TMXAnimationParser instance
        scaling: Scale factor for sprites
        layer_options: Optional layer configuration for arcade.load_tilemap

    Returns:
        arcade.Scene
    """
    Debug.log(f"Loading animated tilemap from parser: {animation_parser.tmx_path}", __file__)

    # Print animation info
    animation_parser.print_animation_info()

    # Create animated sprites
    animated_sprites = animation_parser.create_animated_sprites(scaling)

    # Load the base tilemap using the path from the parser
    tile_map = arcade.load_tilemap(str(animation_parser.tmx_path), scaling, layer_options or {})

    # Create a scene from a tilemap
    scene = arcade.Scene.from_tilemap(tile_map)

    # Track layers that will contain animated sprites
    animated_layers = set()

    # Replace static tiles with animated sprites in their original layers
    if animated_sprites:
        # Get positions of animated tiles grouped by layer
        animated_positions_by_layer = animation_parser.find_animated_tile_positions_by_layer()

        # Process each layer that contains animated tiles
        for layer_name, positions in animated_positions_by_layer.items():
            Debug.log(f"Processing {len(positions)} animated tiles in layer '{layer_name}'", __file__)

            # Track this layer as containing animations
            animated_layers.add(layer_name)

            # Get the corresponding sprite list from the scene
            if layer_name in scene:
                layer_sprites = scene[layer_name]

                # Create positioned animated sprites for this layer
                for tile_id, map_x, map_y in positions:
                    if tile_id in animated_sprites:
                        # Create a new instance of the animated sprite
                        animated_sprite = animated_sprites[tile_id]
                        new_sprite = AnimatedSprite(animated_sprite.textures, 1.0, animated_sprite.frame_durations)
                        if scaling != 1.0:
                            new_sprite.scale = scaling

                        # Position the sprite using map coordinates
                        world_x = (map_x * tile_map.tile_width * scaling) + (tile_map.tile_width * scaling / 2)
                        world_y = ((animation_parser.map_height - 1 - map_y) * tile_map.tile_height * scaling) + (
                                    tile_map.tile_height * scaling / 2)

                        new_sprite.center_x = world_x
                        new_sprite.center_y = world_y

                        # Remove any existing static tile at this position
                        _remove_static_tile_at_position(layer_sprites, world_x, world_y, scaling)

                        # Add the animated sprite to the layer
                        layer_sprites.append(new_sprite)
                        Debug.log(
                            f"Replaced static tile with animated tile {tile_id} at ({map_x}, {map_y}) in layer '{layer_name}'", __file__)

    return scene


def load_animated_tilemap(tmx_file_path: str, scaling: float = 1.0, layer_options: Dict = None):
    """
    Factory function to load a TMX tilemap with animated tiles (compatibility wrapper).

    Args:
        tmx_file_path: Path to the TMX file
        scaling: Scale factor for sprites
        layer_options: Optional layer configuration for arcade.load_tilemap

    Returns:
        arcade.Scene
    """
    # Create parser and delegate to the new function
    animation_parser = TMXAnimationParser(tmx_file_path)
    return load_animated_tilemap_from_parser(animation_parser, scaling, layer_options)


def _remove_static_tile_at_position(sprite_list: arcade.SpriteList, world_x: float, world_y: float,
                                    tolerance: float = 1.0):
    """Remove any static tile sprite at the specified world coordinates"""
    # Find sprites that are close to the target position
    to_remove = []
    for sprite in sprite_list:
        if (abs(sprite.center_x - world_x) < tolerance and
                abs(sprite.center_y - world_y) < tolerance and
                not isinstance(sprite, AnimatedSprite)):  # Don't remove animated tiles
            to_remove.append(sprite)

    # Remove the found sprites
    for sprite in to_remove:
        sprite.remove_from_sprite_lists()
        Debug.log(f"Removed static tile at ({world_x:.1f}, {world_y:.1f})", __file__)

