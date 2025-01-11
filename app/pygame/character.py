from abc import ABC, abstractmethod
from typing import Optional

import pygame
import xml.etree.ElementTree as ET

from pydantic import Field

from app.pygame.config import Config
from app.utilities.dataclasses import Coordinates


class BaseSprite(pygame.sprite.Sprite, ABC):
    def __init__(self, config):
        super().__init__()
        self.config: Config = config

        # Initialize the main rect which will represent the body (rect_A)
        self.body_rect = pygame.Rect(0, 0, 0, 0)
        self.head_rect = pygame.Rect(0, 0, 0, 0)

        self.image: Optional[pygame.Surface] = Field(default=None)
        self.current_direction: str = "down"
        self.current_frame: int = 0
        self.frame_timer: int = 0
        self.move_timer: int = 0

        self.character_frames: dict = {
            'down': {"1": [], "2": [], "3": [], "4": []},
            'left': {"1": [], "2": [], "3": [], "4": []},
            'right': {"1": [], "2": [], "3": [], "4": []},
            'up': {"1": [], "2": [], "3": [], "4": []},
        }

        self.load_character_from_file()

        # Position the body (rect_A) based on the screen
        self.body_rect.x = (self.config.screen_size.x / 2)
        self.body_rect.y = (self.config.screen_size.y / 2)

        # Set rect size based on the body image
        self.body_rect.size = self.image.get_size()

    @property
    @abstractmethod
    def coordinate(self):
        pass

    @abstractmethod
    def load_character_from_file(self):
        pass

    def update(self):

        print(self.character_frames)
        # Get the current body and head images
        current_body_image = self.character_frames[self.current_direction]["2"][self.current_frame][0]
        current_head_image = self.character_frames[self.current_direction]["1"][self.current_frame][0]

        # Create a surface for the body
        self.image = pygame.Surface(
            (current_body_image.get_width(), current_body_image.get_height()),
            pygame.SRCALPHA
        )

        # Blit the body image onto the surface
        self.image.blit(current_body_image, (0, 0))

        # Update the body_rect size based on the body image size
        self.body_rect.size = current_body_image.get_size()

        # Update the head_rect size based on the head image size
        self.head_rect.size = current_head_image.get_size()

        # Position the head_rect relative to the body_rect
        self.head_rect.midbottom = self.body_rect.midtop  # Align head's bottom center to body's top center

    def draw(self):
        # Draw the body using body_rect
        self.config.screen.blit(self.image, self.body_rect.topleft)

        # Now draw the head using head_rect
        self.config.screen.blit(
            self.character_frames[self.current_direction]["1"][self.current_frame][0],
            self.head_rect.topleft
        )

        # Optional: Draw the outline around the body's rect
        # pygame.draw.rect(self.config.screen, (255, 0, 0), self.body_rect, 2)

        # Optional: Draw the outline around the head's rect
        # pygame.draw.rect(self.config.screen, (0, 0, 255), self.head_rect, 2)

    def walking_animation(self):
        """Helper to increment frame timers and cycle frames."""
        self.frame_timer += 1
        if self.frame_timer >= 7:
            self.frame_timer = 0
            frames = self.character_frames[self.current_direction]["1"]
            self.current_frame = (self.current_frame + 1) % len(frames)


class PlayerSprite(BaseSprite):
    def __init__(self, config):
        super().__init__(config)

    @property
    def coordinate(self):
        self.config.char_coord = Coordinates(
            x=((self.body_rect.x + self.config.offset.x) // self.config.tile_size),
            y=((self.body_rect.y + self.config.offset.y) // self.config.tile_size)
        )
        return self.config.char_coord

    def load_character_from_file(self):
        # Parse the .tsx file as XML
        tree = ET.parse(self.config.args.character_location)
        root = tree.getroot()

        tile_width = int(root.attrib['tilewidth']) * self.config.zoom_factor
        tile_height = int(root.attrib['tileheight']) * self.config.zoom_factor
        image_width = int(root.find("image").attrib['width'])

        # Load the tileset image
        tileset_image = pygame.image.load(self.config.args.character_png_location).convert_alpha()

        # Iterate through each tile element in the .tsx file
        for tile in root.findall("tile"):
            properties_element = tile.find('properties')
            if properties_element is not None:
                properties = {prop.attrib['name']: prop.attrib['value']
                              for prop in properties_element.findall('property')}
                direction = properties.get('Direction')
                part = properties.get('Part')

                if direction and part:
                    animation_element = tile.find('animation')
                    if animation_element is not None:
                        # Iterate through each frame in the animation
                        for frame in animation_element.findall('frame'):
                            frame_tile_id = int(frame.attrib['tileid'])
                            duration = int(frame.attrib['duration'])

                            # Calculate the position of the tile in the tileset image
                            tile_x = (frame_tile_id % (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_width // self.config.zoom_factor)
                            tile_y = (frame_tile_id // (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_height // self.config.zoom_factor)

                            # Extract and scale the tile image
                            tile_image = tileset_image.subsurface(
                                pygame.Rect(
                                    tile_x,
                                    tile_y,
                                    tile_width // self.config.zoom_factor,
                                    tile_height // self.config.zoom_factor)
                            )
                            scaled_tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

                            # Append the frame to the appropriate direction and part
                            self.character_frames[direction][part].append((scaled_tile_image, duration))

        # Initialize the first frame of the character
        self.update()


class NPCSprite(BaseSprite):
    def __init__(self, config):
        super().__init__(config)

    def coordinate(self):
        pass

    def load_character_from_file(self):
        # Parse the .tsx file as XML
        tree = ET.parse(self.config.args.npc_location)
        root = tree.getroot()

        tile_width = int(root.attrib['tilewidth']) * self.config.zoom_factor
        tile_height = int(root.attrib['tileheight']) * self.config.zoom_factor
        image_width = int(root.find("image").attrib['width'])

        # Load the tileset image
        tileset_image = pygame.image.load(self.config.args.npc_png_location).convert_alpha()

        # Iterate through each tile element in the .tsx file
        for tile in root.findall("tile"):
            properties_element = tile.find('properties')
            if properties_element is not None:
                properties = {prop.attrib['name']: prop.attrib['value']
                              for prop in properties_element.findall('property')}
                direction = properties.get('Direction')
                part = properties.get('Part')

                if direction and part:
                    animation_element = tile.find('animation')
                    if animation_element is not None:
                        # Iterate through each frame in the animation
                        for frame in animation_element.findall('frame'):
                            frame_tile_id = int(frame.attrib['tileid'])
                            duration = int(frame.attrib['duration'])

                            # Calculate the position of the tile in the tileset image
                            tile_x = (frame_tile_id % (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_width // self.config.zoom_factor)
                            tile_y = (frame_tile_id // (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_height // self.config.zoom_factor)

                            # Extract and scale the tile image
                            tile_image = tileset_image.subsurface(
                                pygame.Rect(
                                    tile_x,
                                    tile_y,
                                    tile_width // self.config.zoom_factor,
                                    tile_height // self.config.zoom_factor)
                            )
                            scaled_tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

                            # Append the frame to the appropriate direction and part
                            self.character_frames[direction][part].append((scaled_tile_image, duration))

        # Initialize the first frame of the character
        self.update()
