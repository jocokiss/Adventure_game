"""Module containing common utility functions."""
from src.utilities.dataclasses import Coordinates


def half_coordinates(screen_size: "Coordinates", tile_size: int) -> tuple[int, int]:
    # Calculate half of the screen width and height in tiles
    return (
        (screen_size.x // tile_size) // 2,
        (screen_size.y // tile_size) // 2
    )


def get_xp_level(xp_percentage: int) -> int:
    # Adjust the logic to handle ranges explicitly
    if xp_percentage == 100:
        return 4
    elif 75 <= xp_percentage < 100:
        return 3
    elif 50 <= xp_percentage < 75:
        return 2
    elif 25 <= xp_percentage < 50:
        return 1
    else:
        return 0


def calculate_required_xp(lvl: int) -> int:
    """Calculate the XP required for the given level."""
    a = 50  # Controls how steeply the XP curve increases
    b = 100  # Base XP increment
    return a * lvl ** 2 + b * lvl
