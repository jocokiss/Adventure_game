import pygame

from src.gameplay.combat.combat_attr import CombatAttributes
from src.gameplay.config import Config
from src.utilities.common_utils import get_xp_level
from src.utilities.dataclasses import Coordinates
from src.utilities.tiled import Tiled


class GameUI:
    def __init__(self, config: Config, stats: CombatAttributes):
        self.config = config
        self.player_stats = stats

        self.screen = self.config.screen

        self.bar_scale = float(self.config.args.ui_scale) * self.config.tile_size
        self.acc_scale = int(self.bar_scale / 3 * 2)

        self.__set_plate_coordinates()

        self.tiled = Tiled.from_tileset(self.config, "objects")
        self.tiled.load()

    def __load_frames(self, object_name: str, scale: int):
        frames = self.tiled.static_frames.get_frames(object_name)
        # Map parts to tile images
        part_to_tile = {frame.part: frame.image for frame in frames}
        # Pre-bar_scale the images
        return {part: pygame.transform.scale(image, (scale,) * 2)
                for part, image in part_to_tile.items()}

    def __set_plate_coordinates(self, start_x: int = 20, start_y: int = 20):
        self.plate_coordinates = Coordinates((
            start_x,
            start_y
        ))

        self.heart_coordinates = Coordinates((
            int(start_x + self.bar_scale * 2),
            int(start_y + self.bar_scale * 2) - self.bar_scale // 10,
        ))

        self.number_coordinates = Coordinates((
            int(start_x + self.bar_scale // 4),
            int(start_y + self.bar_scale * 2),
        ))

        self.xp_bar_coordinates = Coordinates((
            int(start_x + self.bar_scale),
            int(start_y + 2 * self.bar_scale)
        ))

    def __render_health(self) -> None:
        images = self.__load_frames("health", self.acc_scale)
        positions = [
            (self.heart_coordinates.x + self.acc_scale * i, self.heart_coordinates.y) for i in range(4)
        ]
        # Render empty hearts as the background
        for position in positions:
            self.screen.blit(images["5"], position)

        full_hearts = self.player_stats.health_percentage // 25
        remainder = self.player_stats.health_percentage % 25

        # Render full hearts
        for i in range(full_hearts):
            self.screen.blit(images["1"], positions[i])

        # Render partial heart, if applicable
        if remainder > 0 and full_hearts < len(positions):
            pos = positions[full_hearts]
            partial_part = (
                "4" if remainder <= 25 / 3 else
                "3" if remainder <= (25 / 3) * 2 else
                "2"
            )
            self.screen.blit(images[partial_part], pos)

    def __render_level(self) -> None:
        split_digits = tuple(digit for digit in str(self.player_stats.level))
        images = self.__load_frames("numbers", self.acc_scale)
        for digit in split_digits:
            number_image = images.get(digit)
            # Scale the bar_tile image
            index = split_digits.index(digit)
            # Calculate the position
            x = self.number_coordinates.x + (index * self.acc_scale / 2)
            y = self.number_coordinates.y

            # Render the bar_tile
            self.screen.blit(number_image, (x, y))

    def __render_plate(self) -> None:
        """
        Render the XP bar by assembling tiles dynamically based on the PART attribute.
        """
        images = self.__load_frames("level_bar", self.bar_scale)
        for key in sorted(images.keys(), key=int):  # Sort keys numerically
            index = int(key) - 1  # Convert key to zero-based index
            tile = images[key]  # Access the corresponding image

            row = index // 5  # Determine row
            col = index % 5  # Determine column

            # Calculate the position
            x = self.plate_coordinates.x + (col * self.bar_scale)
            y = self.plate_coordinates.y + (row * self.bar_scale)

            # Render the tile
            self.screen.blit(tile, (x, y))
        self.__render_xp_bar()

    def __render_xp_bar(self) -> None:
        """
        Render the XP bar dynamically based on the current XP percentage.
        """
        images = self.__load_frames("xp_bar", self.bar_scale)
        positions = [(self.xp_bar_coordinates.x + self.bar_scale * i, self.xp_bar_coordinates.y) for i in range(4)]
        # Determine how many tiles to render

        if bar_length := get_xp_level(self.player_stats.xp_percentage):
            for i in range(bar_length):
                tile_key = str(i + 1)
                if tile_key in images:
                    self.screen.blit(images[tile_key], positions[i])
                else:
                    print(f"Tile for part '{tile_key}' not found!")

    def draw(self):
        """Draw the UI elements."""
        self.__render_plate()
        self.__render_level()
        self.__render_health()
    