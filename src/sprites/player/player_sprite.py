import pygame

from src.sprites.base_sprite import BaseSprite
from src.utilities.dataclasses import Coordinates
from src.utilities.tiled import Tiled


class PlayerSprite(BaseSprite):
    def __init__(self, config):
        super().__init__(config)
        self.tiled = Tiled.from_tileset(self.config, "character")
        self.tiled.load()
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
        body_frames = self.tiled.animated_frames.get_frames(self.state, self.current_direction, "2")
        head_frames = self.tiled.animated_frames.get_frames(self.state, self.current_direction, "1")

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
        head_frames = self.tiled.animated_frames.get_frames(self.state, self.current_direction, "1")
        if head_frames:
            self.config.screen.blit(head_frames[self.current_frame].image, self.head_rect.topleft)

    def walking_animation(self):
        """Increment frame timers and cycle through animation frames."""
        self.frame_timer += 1
        body_frames = self.tiled.animated_frames.get_frames(self.state, self.current_direction, "2")
        if not body_frames:
            return  # No frames available for this animation

        if self.frame_timer >= 7:  # Adjust timer threshold as needed
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(body_frames)
