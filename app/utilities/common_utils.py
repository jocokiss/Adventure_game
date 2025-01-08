"""Module containing common utility functions."""
from app.utilities.dataclasses import Coordinates


def half_coordinates(screen_size: "Coordinates", tile_size: int) -> tuple[int, int]:
    # Calculate half of the screen width and height in tiles
    return (
        (screen_size.x // tile_size) // 2,
        (screen_size.y // tile_size) // 2
    )
