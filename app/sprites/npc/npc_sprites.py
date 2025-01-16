import random

import pygame

from app.sprites.base_sprite import BaseSprite
from app.utilities.dataclasses import Coordinates, NPCAttributes


class NPCSprite(BaseSprite):
    def __init__(self, config, initial_position: tuple[int, int], attributes: NPCAttributes = NPCAttributes()):
        super().__init__(config)
        self.tsx_location = self.config.args.npc_location
        self.png_location = self.config.args.npc_png_location

        self.load_character_from_file()

        self.position = pygame.Vector2(initial_position)  # Map position (in tiles)
        self.previous_position = self.position.copy()

        self.attributes = attributes

        if self.attributes.is_stationary:
            self.config.no_go_zone.add(initial_position)

        # Other attributes from the dataclass
        self.state = self.attributes.state
        self.interaction_range = self.attributes.interaction_range
        self.patrol_path = self.attributes.patrol_path
        self.current_patrol_index = self.attributes.current_patrol_index
        self.is_random_movement = self.attributes.is_random_movement

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

    def interact(self, player_position):
        """Handle interaction with the NPC."""
        distance = self.position.distance_to(player_position)
        if distance <= self.interaction_range and self.state == "ASLEEP":
            self.state = "IDLE"  # Transition to awake state
            self.current_frame = 0  # Reset animation frame for waking animation

    def update(self):
        """Update the NPC's image and position on the map."""

        if self.state == "ASLEEP":
            self.update_sleeping()
        elif self.state == "IDLE":
            self.update_idle()
        elif self.state == "ACTIVE":
            self.update_active()

            # Determine direction for animation if moving
            self.determine_direction()

            # Default to "down" if the current direction has no frames for this state
        direction_to_use = self.current_direction
        if self.state in ["ASLEEP", "IDLE"] and self.current_direction not in ["DOWN"]:
            direction_to_use = "DOWN"

        # Get frames for the current direction and all parts
        top_left_frames = self.frames.get_frames(self.state, direction_to_use, "1")
        top_right_frames = self.frames.get_frames(self.state, direction_to_use, "2")
        bottom_left_frames = self.frames.get_frames(self.state, direction_to_use, "3")
        bottom_right_frames = self.frames.get_frames(self.state, direction_to_use, "4")

        # Ensure all required frames are available
        if not (top_left_frames and top_right_frames and bottom_left_frames and bottom_right_frames):
            raise ValueError(f"Missing frames for direction {direction_to_use} in action {self.state}")

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

    def update_sleeping(self):
        """Update the NPC's sleeping behavior."""
        self.sleep_timer += self.config.dt
        if self.sleep_timer >= 250:  # Adjust frame speed for sleep animation
            self.sleep_timer = 0
            self.current_frame = (self.current_frame + 1) % len(
                self.frames.get_frames("ASLEEP", "DOWN", "1")
            )

    def update_idle(self):
        """Handle the idle animation."""
        # Get the idle frames for the "DOWN" direction
        idle_frames = self.frames.get_frames("IDLE", "DOWN", "1")
        if not idle_frames:
            raise ValueError("No idle frames found for direction DOWN.")

        # Increment the timer for animation
        self.sleep_timer += self.config.dt
        if self.sleep_timer >= 250:  # Idle animation frame speed
            self.sleep_timer = 0  # Reset the timer
            self.current_frame = (self.current_frame + 1) % len(idle_frames)  # Loop through frames

    def update_active(self):
        """Update NPC's movement and active behavior."""
        self.update_movement()

    def move_randomly(self):
        """Move the NPC randomly on the map."""
        self.move_timer += self.config.dt
        if self.move_timer >= 1000:  # Move every 1 second
            self.move_timer = 0
            self.previous_position = self.position.copy()  # Update previous position

            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random direction
            new_x = self.position.x + dx
            new_y = self.position.y + dy

            # Check if the new position is within the map boundaries
            if 0 <= new_x < self.config.map_data.width and 0 <= new_y < self.config.map_data.height:
                self.position.update(new_x, new_y)

    def patrol(self):
        """Follow a predefined patrol path."""
        self.move_timer += self.config.dt
        if self.move_timer >= 1000:  # Move every 1 second
            self.move_timer = 0
            self.previous_position = self.position.copy()  # Update previous position

            if self.patrol_path:
                self.position.update(self.patrol_path[self.current_patrol_index])
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_path)

    def walking_animation(self):
        """Increment frame timers and cycle through frames."""
        self.frame_timer += self.config.dt
        body_frames = self.frames.get_frames(self.state, self.current_direction, "2")
        if not body_frames:
            return  # No frames available for this animation

        if self.frame_timer >= 500:  # Adjust timer threshold as needed
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

        screen_y -= 44

        self.config.screen.blit(self.image, (screen_x, screen_y))
