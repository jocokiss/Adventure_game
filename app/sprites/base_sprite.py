import random
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional

import pygame
import xml.etree.ElementTree as ET

from pydantic import Field

from app.pygame.config import Config
from app.utilities.dataclasses import Coordinates, AnimationFrame, NPCAttributes


class BaseSprite(pygame.sprite.Sprite, ABC):
    def __init__(self, config):
        super().__init__()
        self.config: Config = config

        self.tsx_location: str = ""
        self.png_location: str = ""

        self.frames = SpriteFrames()

        # Initialize the main rect which will represent the body (rect_A)
        self.body_rect = pygame.Rect(0, 0, 0, 0)
        self.head_rect = pygame.Rect(0, 0, 0, 0)

        self.image: Optional[pygame.Surface] = Field(default=None)
        self.state: str = 'WALK'
        self.current_direction: str = "DOWN"
        self.current_frame: int = 0
        self.frame_timer: int = 0
        self.sleep_timer: int = 0
        self.move_timer: int = 0

    @property
    @abstractmethod
    def coordinate(self):
        pass

    def load_character_from_file(self) -> None:
        """Loads character animations from a TSX file and a PNG image."""
        # Parse the TSX file and load the image
        tree = ET.parse(self.tsx_location)
        root = tree.getroot()
        image = pygame.image.load(self.png_location).convert_alpha()

        # Pre-calculate common values
        tileset_width = int(root.find("image").attrib["width"])
        tiles_per_row = tileset_width // self.config.base_tile_size

        # Iterate through each <tile> element
        for tile in root.findall("tile"):
            # Fetch tile properties
            props_element = tile.find("properties")
            if not props_element:
                continue

            props = {
                p.attrib["name"]: p.attrib["value"]
                for p in props_element.findall("property")
            }

            action = props.get("Action")
            direction = props.get("Direction")
            part = props.get("Part")
            if not (action and direction and part):
                continue

            # Find the <animation> element
            animation_element = tile.find("animation")
            if not animation_element:
                continue

            # Parse each frame in the animation
            for frame in animation_element.findall("frame"):
                frame_id = int(frame.attrib["tileid"])
                duration = int(frame.attrib["duration"])

                # Calculate tile position in the source image
                tile_x = (frame_id % tiles_per_row) * self.config.base_tile_size
                tile_y = (frame_id // tiles_per_row) * self.config.base_tile_size

                # Extract and scale the tile image
                tile_image = image.subsurface(
                    (tile_x, tile_y, self.config.base_tile_size, self.config.base_tile_size)
                )
                scaled_tile_image = pygame.transform.scale(
                    tile_image, (self.config.tile_size, self.config.tile_size)
                )

                # Create an AnimationFrame and add it to the animations
                animation_frame = AnimationFrame(
                    image=scaled_tile_image,
                    duration=duration
                )
                self.frames.add_frame(
                    animation=action,
                    direction=direction,
                    part=part,
                    frame=animation_frame
                )

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        """Draw the body and head parts of the sprite on the screen."""
        pass

    @abstractmethod
    def walking_animation(self):
        """Increment frame timers and cycle through animation frames."""
        pass


class SpriteFrames:
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
