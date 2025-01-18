import pygame
import xml.etree.ElementTree as ET

from app.utilities.tiled import Tiled


class GameUI:
    def __init__(self, config):
        self.config = config
        self.tiled = Tiled.from_tileset(self.config, "objects")
        self.tiled.load()

    def __render_xp_bar(self, screen, bar_key="5x4", parts_count=20, tiles_per_row=5, start_x=20, start_y=20):
        """
        Render the XP bar by assembling tiles dynamically.

        Args:
            screen: The Pygame screen to draw on.
            bar_key: Key in the static_frames for the XP bar tiles.
            parts_count: Total number of parts of the XP bar.
            tiles_per_row: Number of tiles per row.
            start_x: X-coordinate to start drawing the bar.
            start_y: Y-coordinate to start drawing the bar.
        """
        bar_tiles = self.tiled.static_frames.get_objects_by_size(5, 4).get(bar_key, None)
        if not bar_tiles:
            print(f"XP bar with key '{bar_key}' not found!")
            return

        # Use the first tile (if multiple are available, pick the one needed)
        bar_tile = bar_tiles[0].image
        tile_width = bar_tile.get_width()
        tile_height = bar_tile.get_height()

        # Draw the XP bar by assembling tiles
        for index in range(parts_count):
            row = index // tiles_per_row  # Determine row
            col = index % tiles_per_row  # Determine column
            x = start_x + (col * tile_width)
            y = start_y + (row * tile_height)
            screen.blit(bar_tile, (x, y))

    def draw(self, screen, player):
        """Draw the UI elements."""
        # Draw the level bar
        lvl_bar = self.tiled.static_frames.get("lvl_bar", None)
        if lvl_bar:
            bar_x = 20  # Position from the top-left corner
            bar_y = 20
            num_tiles = 10  # Number of tiles in the level bar
            filled_tiles = int((player.combat.level / player.combat.max_level) * num_tiles)

            # Draw each tile of the level bar
            for i in range(num_tiles):
                tile_x = bar_x + (i * lvl_bar.get_width())
                if i < filled_tiles:
                    # Draw filled tile
                    screen.blit(lvl_bar, (tile_x, bar_y))
                else:
                    # Draw empty or background tile (optional)
                    empty_tile = self.tiled.static_frames.get("empty_bar_tile", None)
                    if empty_tile:
                        screen.blit(empty_tile, (tile_x, bar_y))

        # Render the player's level next to the bar
        level = str(player.combat.level)  # Convert level to string for multi-digit support
        digit_width = self.config.tile_size // 2  # Scale digits appropriately
        digit_height = self.config.tile_size // 2

        # Position for level digits
        digit_x = bar_x + (num_tiles * lvl_bar.get_width()) + 10  # Next to the bar
        digit_y = bar_y + (lvl_bar.get_height() // 2) - (digit_height // 2)

        # Draw each digit using tileset tiled.static_frames
        for digit in level:
            digit_icon = self.tiled.static_frames.get(f"number_{digit}", None)
            if digit_icon:
                scaled_digit = pygame.transform.scale(digit_icon, (digit_width, digit_height))
                screen.blit(scaled_digit, (digit_x, digit_y))
                digit_x += digit_width  # Adjust x-position for the next digit
