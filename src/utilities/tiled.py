from collections import defaultdict
from typing import Dict, List, Tuple

from src.utilities.dataclasses import AnimationFrame, ObjectFrame  # Assuming you have this class

import pygame
import xml.etree.ElementTree as ET


class Tiled:
    def __init__(self, config, root, image):
        """
        Initialize the Tiled class.

        Args:
            config: The configuration object.
            root: The root element of the parsed TSX file.
            image: The loaded image from the tileset.
        """
        self.config = config
        self.tiles = root.findall("tile")
        self.image = image  # The loaded tileset image

        self.animated_frames = AnimatedObjects()  # For animations
        self.static_frames = StaticObjects()  # For static images

        self.tileset_width = int(root.find("image").attrib["width"])
        self.tiles_per_row = self.tileset_width // self.config.base_tile_size

    @classmethod
    def from_tileset(cls, config, tileset):
        """
        Initialize the Tiled class by loading the TSX and PNG files.

        Args:
            config: The configuration object containing paths.
            tileset: The name of the tileset file (without extension).

        Returns:
            An instance of the Tiled class.
        """
        tsx_path = config.args.tiled_folder + tileset + ".tsx"
        png_path = config.args.tiled_folder + "tileset/" + tileset + ".png"

        # Parse the TSX file and load the image
        tree = ET.parse(tsx_path)
        root = tree.getroot()
        image = pygame.image.load(png_path).convert_alpha()

        return cls(config, root, image)

    def load(self):
        """Iterate through tiles and process them."""
        for tile in self.tiles:
            props = self.__extract_properties(tile)
            tile_type = tile.attrib.get("type")
            if not tile_type or not props:
                continue

            if tile_type == "Sprite":
                animation_element = tile.find("animation")
                if animation_element:
                    self.__handle_sprites(animation_element, props)
            elif tile_type == "Object":
                self.__handle_objects(tile, props)

    @staticmethod
    def __extract_properties(tile):
        """Extract properties from a tile."""
        props_element = tile.find("properties")
        if not props_element:
            return {}

        return {
            p.attrib["name"]: p.attrib["value"]
            for p in props_element.findall("property")
        }

    def __handle_sprites(self, animation_element, props):
        """Process sprite animations."""
        action, direction, part = props.get("Action"), props.get("Direction"), props.get("Part")
        if not (action and direction and part):
            return

        for frame in animation_element.findall("frame"):
            frame_id, duration = int(frame.attrib["tileid"]), int(frame.attrib["duration"])
            scaled_tile_image = self.__extract_tile_image(frame_id)

            self.animated_frames.add_frame(
                animation=action,
                direction=direction,
                part=part,
                frame=AnimationFrame(image=scaled_tile_image, duration=duration)
            )

    def __handle_objects(self, tile, props):
        """Process static objects."""
        name, part = props.get("UIElement"), props.get("Part")
        width, height = int(props.get("Width", 0)), int(props.get("Height", 0))
        if not (name and part and width and height):
            return

        tile_id = int(tile.attrib["id"])
        scaled_tile_image = self.__extract_tile_image(tile_id)

        self.static_frames.add_frame(
            object_name=name,
            frame=ObjectFrame(image=scaled_tile_image, part=part)
        )

    def __extract_tile_image(self, tile_id):
        """Extract and scale tile image."""
        tile_x = (tile_id % self.tiles_per_row) * self.config.base_tile_size
        tile_y = (tile_id // self.tiles_per_row) * self.config.base_tile_size

        tile_image = self.image.subsurface(
            (tile_x, tile_y, self.config.base_tile_size, self.config.base_tile_size)
        )
        return pygame.transform.scale(tile_image, (self.config.tile_size, self.config.tile_size))


class StaticObjects:
    """Manages object frames, organizing them by name."""

    def __init__(self):
        """
        Initializes the storage for object frames.

        Attributes:
            objects (defaultdict): Dictionary structure where:
                - Key: Object name (e.g., "house", "tree").
                - Value: List of ObjectFrame instances for that object.
        """
        self.objects: Dict[str, List[ObjectFrame]] = defaultdict(list)

    def add_frame(self, object_name: str, frame: ObjectFrame):
        """
        Adds a frame to the storage, categorized by object name.

        Args:
            object_name (str): Name of the object (e.g., "house").
            frame (ObjectFrame): The frame to add.
        """
        self.objects[object_name].append(frame)

    def get_frames(self, object_name: str) -> List[ObjectFrame]:
        """
        Retrieves all frames for a specific object by its name.

        Args:
            object_name (str): Name of the object (e.g., "house").

        Returns:
            List[ObjectFrame]: List of frames for the specified object.
        """
        return self.objects[object_name] \
            if self.objects[object_name] \
            else print(f"Frames for key '{object_name}' not found!")

    def __repr__(self):
        """
        Returns a string representation of the stored objects, organized by name.
        """
        repr_str = "StaticObjects:\n"
        for obj_name, frames in self.objects.items():
            repr_str += f"  {obj_name}: {len(frames)} frame(s)\n"
        return repr_str


class AnimatedObjects:
    """Manages sprite animations, organizing frames by animation, direction, and part."""

    def __init__(self):
        """
        Initializes the animation storage.

        Attributes:
            animations (defaultdict): Nested dictionary structure where:
                - Outer key: Animation name (e.g., "walk", "idle").
                - Middle key: Direction (e.g., "up", "down", "left", "right").
                - Inner key: Part of the sprite (e.g., "1" for head, "2" for body).
                - Value: List of frames (e.g., instances of AnimationFrame).
        """
        self.frames = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def add_frame(self, animation: str, direction: str, part: str, frame):
        """
        Adds a frame to the animation storage.

        Args:
            animation (str): Name of the animation (e.g., "walk", "idle").
            direction (str): Direction of the animation (e.g., "up", "down").
            part (str): Part of the sprite (e.g., "1" for head, "2" for body).
            frame: An instance of AnimationFrame containing the image and duration.

        Example:
            animations = SpriteAnimations()
            animations.add_frame(
                animation="walk",
                direction="down",
                part="2",
                frame=AnimationFrame(image=surface, duration=100)
            )
        """
        self.frames[animation][direction][part].append(frame)

    def get_frames(self, animation: str, direction: str, part: str) -> list:
        """
        Retrieves all frames for a given animation, direction, and part.

        Args:
            animation (str): Name of the animation (e.g., "walk").
            direction (str): Direction of the animation (e.g., "left").
            part (str): Part of the sprite (e.g., "1").

        Returns:
            List: A list of frames for the specified animation, direction, and part.

        Raises:
            KeyError: If the specified animation, direction, or part does not exist.

        Example:
            frames = animations.get_frames("walk", "down", "1")
            for frame in frames:
                print(frame.image, frame.duration)
        """
        return self.frames[animation][direction][part]
