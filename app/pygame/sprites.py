import random
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional

import pygame
import xml.etree.ElementTree as ET

from pydantic import Field

from app.pygame.config import Config
from app.utilities.dataclasses import Coordinates, AnimationFrame


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
        self.current_action: str = 'walk'
        self.current_direction: str = "down"
        self.current_frame: int = 0
        self.frame_timer: int = 0
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


class PlayerSprite(BaseSprite):
    def __init__(self, config):
        super().__init__(config)

        self.tsx_location = self.config.args.character_location
        self.png_location = self.config.args.character_png_location

        self.load_character_from_file()
        self.update()

        # Position the body (rect_A) based on the screen
        self.body_rect.x = (self.config.screen_size.x / 2)
        self.body_rect.y = (self.config.screen_size.y / 2)

        # Set rect size based on the body image
        self.body_rect.size = self.image.get_size()

    @property
    def coordinate(self):
        self.config.char_coord = Coordinates(
            x=((self.body_rect.x + self.config.offset.x) // self.config.tile_size),
            y=((self.body_rect.y + self.config.offset.y) // self.config.tile_size)
        )
        return self.config.char_coord

    def update(self):
        """Update the current body and head images based on the animation and direction."""
        # Get frames for the current direction and part
        body_frames = self.frames.get_frames(self.current_action, self.current_direction, "2")
        head_frames = self.frames.get_frames(self.current_action, self.current_direction, "1")

        if not body_frames or not head_frames:
            raise ValueError(f"No frames found for direction {self.current_direction}")

        # Get the current frames for body and head
        current_body_frame = body_frames[self.current_frame]
        current_head_frame = head_frames[self.current_frame]

        # Create a surface for the body
        self.image = pygame.Surface(
            (current_body_frame.image.get_width(), current_body_frame.image.get_height()),
            pygame.SRCALPHA
        )

        # Blit the body image onto the surface
        self.image.blit(current_body_frame.image, (0, 0))

        # Update the body_rect size based on the body image size
        self.body_rect.size = current_body_frame.image.get_size()

        # Update the head_rect size based on the head image size
        self.head_rect.size = current_head_frame.image.get_size()

        # Position the head_rect relative to the body_rect
        self.head_rect.midbottom = self.body_rect.midtop  # Align head's bottom center to body's top center

    def draw(self):
        """Draw the body and head parts of the sprite on the screen."""
        # Draw the body using body_rect
        self.config.screen.blit(self.image, self.body_rect.topleft)

        # Draw the head using head_rect
        head_frames = self.frames.get_frames(self.current_action, self.current_direction, "1")
        if head_frames:
            self.config.screen.blit(head_frames[self.current_frame].image, self.head_rect.topleft)

    def walking_animation(self):
        """Increment frame timers and cycle through animation frames."""
        self.frame_timer += 1
        body_frames = self.frames.get_frames(self.current_action, self.current_direction, "2")
        if not body_frames:
            return  # No frames available for this animation

        if self.frame_timer >= 7:  # Adjust timer threshold as needed
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(body_frames)


class NPCSprite(BaseSprite):
    def __init__(self, config, initial_position):
        super().__init__(config)
        self.tsx_location = self.config.args.npc_location
        self.png_location = self.config.args.npc_png_location

        self.load_character_from_file()

        self.position = pygame.Vector2(initial_position)  # Map position (in tiles)
        self.previous_position = self.position.copy()

        self.movement_timer = 0  # Tracks time between movement steps
        self.patrol_path = []  # List of positions for patrolling
        self.current_patrol_index = 0
        self.is_random_movement = True  # Toggle for random vs. patrolling

    @property
    def coordinate(self):
        """Convert NPC's map position to screen coordinates for collision detection."""
        return Coordinates(
            x=int(self.position.x),
            y=int(self.position.y)
        )

    def determine_direction(self):
        """Determine the direction based on position change."""
        dx = self.position.x - self.previous_position.x
        dy = self.position.y - self.previous_position.y

        if dx > 0:
            self.current_direction = "right"
        elif dx < 0:
            self.current_direction = "left"
        elif dy > 0:
            self.current_direction = "down"
        elif dy < 0:
            self.current_direction = "up"

    def update(self):
        """Update the NPC's image and position on the map."""
        # Get frames for the current direction and all parts
        top_left_frames = self.frames.get_frames(self.current_action, self.current_direction, "1")
        top_right_frames = self.frames.get_frames(self.current_action, self.current_direction, "2")
        bottom_left_frames = self.frames.get_frames(self.current_action, self.current_direction, "3")
        bottom_right_frames = self.frames.get_frames(self.current_action, self.current_direction, "4")

        # Ensure all required frames are available
        if not (top_left_frames and top_right_frames and bottom_left_frames and bottom_right_frames):
            raise ValueError(f"Missing frames for direction {self.current_direction} in action {self.current_action}")

        # Get the current frame for each part
        current_top_left = top_left_frames[self.current_frame]
        current_top_right = top_right_frames[self.current_frame]
        current_bottom_left = bottom_left_frames[self.current_frame]
        current_bottom_right = bottom_right_frames[self.current_frame]

        # Determine the dimensions of the combined 2x2 grid
        tile_width = current_top_left.image.get_width()
        tile_height = current_top_left.image.get_height()
        total_width = tile_width * 2  # 2 tiles wide
        total_height = tile_height * 2  # 2 tiles tall

        # Create a surface for the combined sprite
        self.image = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        # Blit the 2x2 grid onto the combined surface
        self.image.blit(current_top_left.image, (0, 0))  # Top-left
        self.image.blit(current_top_right.image, (tile_width, 0))  # Top-right
        self.image.blit(current_bottom_left.image, (0, tile_height))  # Bottom-left
        self.image.blit(current_bottom_right.image, (tile_width, tile_height))  # Bottom-right

        # Update the body_rect size based on the combined image
        self.body_rect.size = self.image.get_size()

        # Update the NPC's position on the screen relative to the map and camera offset
        self.body_rect.x = int(self.position.x * self.config.tile_size - self.config.offset.x)
        self.body_rect.y = int(self.position.y * self.config.tile_size - self.config.offset.y)

    def move_randomly(self):
        """Move the NPC randomly on the map."""
        self.movement_timer += self.config.dt
        if self.movement_timer >= 1000:  # Move every 1 second
            self.movement_timer = 0
            self.previous_position = self.position.copy()  # Update previous position

            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random direction
            new_x = self.position.x + dx
            new_y = self.position.y + dy

            # Check if the new position is within the map boundaries
            if 0 <= new_x < self.config.map_data.width and 0 <= new_y < self.config.map_data.height:
                self.position.update(new_x, new_y)

    def patrol(self):
        """Follow a predefined patrol path."""
        self.movement_timer += self.config.dt
        if self.movement_timer >= 1000:  # Move every 1 second
            self.movement_timer = 0
            self.previous_position = self.position.copy()  # Update previous position

            if self.patrol_path:
                self.position.update(self.patrol_path[self.current_patrol_index])
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_path)

    def walking_animation(self):
        """Increment frame timers and cycle through frames."""
        self.frame_timer += self.config.dt
        body_frames = self.frames.get_frames(self.current_action, self.current_direction, "2")
        if not body_frames:
            return  # No frames available for this animation

        if self.frame_timer >= 250:  # Adjust timer threshold as needed
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(body_frames)

    def update_movement(self):
        """Update NPC movement."""
        if self.is_random_movement:
            self.move_randomly()
        else:
            self.patrol()

        # Determine direction based on position change
        self.determine_direction()

        # Update animation frame
        self.walking_animation()

    def draw(self):
        """Draw the NPC on the screen."""
        screen_x = self.position.x * self.config.tile_size - self.config.offset.x
        screen_y = self.position.y * self.config.tile_size - self.config.offset.y
        self.config.screen.blit(self.image, (screen_x, screen_y))
