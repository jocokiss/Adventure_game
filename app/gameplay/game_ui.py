import pygame

from app.utilities.tiled import Tiled


class GameUI:
    def __init__(self, config):
        self.config = config
        self.screen = self.config.screen

        self.scale = float(self.config.args.ui_scale)

        self.tiled = Tiled.from_tileset(self.config, "objects")
        self.tiled.load()

    def __render_health(self):
        hearts = self.tiled.static_frames.get_objects_by_size(1, 1).get("health", None)
        if not hearts:
            print("Numbers with key 'health' not found!")
            return

        # Map parts to tile images
        part_to_tile = {tile.part: tile.image for tile in hearts}
        if not all(key in part_to_tile for key in ["1", "2", "3", "4", "5"]):
            print("One or more heart parts are missing!")
            return

        # Pre-scale the images
        scaled_images = {
            part: pygame.transform.scale(image, (int(image.get_width() * 0.5), int(image.get_height() * 0.5)))
            for part, image in part_to_tile.items()
        }

        # Define heart positions
        positions = [(115 + 35 * space, 110) for space in range(4)]

        # Render empty hearts as the background
        for position in positions:
            self.screen.blit(scaled_images["5"], position)

        # Calculate the number of full and partial hearts
        health_percentage = 25    # TODO: Swap for actual data

        full_hearts = health_percentage // 25
        remainder = health_percentage % 25

        # Render full hearts
        for i in range(full_hearts):
            self.screen.blit(scaled_images["1"], positions[i])

        # Render partial heart, if applicable
        if remainder > 0 and full_hearts < len(positions):
            pos = positions[full_hearts]
            partial_part = (
                "4" if remainder <= 25 / 3 else
                "3" if remainder <= (25 / 3) * 2 else
                "2"
            )
            self.screen.blit(scaled_images[partial_part], pos)

    def __render_level(self):
        numbers = self.tiled.static_frames.get_objects_by_size(1, 1).get("numbers", None)
        if not numbers:
            print(f"Numbers with key '{numbers}' not found!")
            return

        level = 1
        split_digits = tuple(digit for digit in str(level))

        start_x, start_y = 30, 116

        for index, digit in enumerate(split_digits):
            tile = next((tile for tile in numbers if tile.part == digit), None)
            # Calculate scaled width and height
            scaled_width = int(tile.image.get_width() * 0.5)
            scaled_height = int(tile.image.get_height() * 0.5)

            # Scale the tile image
            scaled_tile = pygame.transform.scale(tile.image, (scaled_width, scaled_height))

            # Calculate the position
            x = start_x + ((index * scaled_width) // 2)
            y = start_y

            # Render the tile
            self.screen.blit(scaled_tile, (x, y))

    def __level_plate(
            self, bar_key="lvl_bar", parts_count=20, tiles_per_row=5, start_x=20, start_y=20
    ):
        """
        Render the XP bar by assembling tiles dynamically based on the PART attribute.

        Args:
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

        # Sort tiles by their PART attribute to ensure correct order
        sorted_tiles = sorted(bar_tiles, key=lambda tile: int(tile.part))
        if len(sorted_tiles) != parts_count:
            print(
                f"Warning: Expected {parts_count} tiles but found {len(sorted_tiles)} for bar '{bar_key}'"
            )

        # Draw the XP bar by assembling tiles
        for index, tile in enumerate(sorted_tiles):
            row = index // tiles_per_row  # Determine row
            col = index % tiles_per_row  # Determine column

            # Calculate scaled width and height
            scaled_width = int(tile.image.get_width() * self.scale)
            scaled_height = int(tile.image.get_height() * self.scale)

            # Scale the tile image
            scaled_tile = pygame.transform.scale(tile.image, (scaled_width, scaled_height))

            # Calculate the position
            x = start_x + (col * scaled_width)
            y = start_y + (row * scaled_height)

            # Render the tile
            self.screen.blit(scaled_tile, (x, y))

    def draw(self):
        """Draw the UI elements."""
        # Draw the level bar
        self.__level_plate()
        self.__render_level()
        self.__render_health()


class Heart:
    x: int = 0
    y: int = 0
    tile_image: pygame.Surface = None
    