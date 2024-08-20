import pygame
import pytmx

from app.utilities.arg_parser import ArgParser
from app.utilities.dataclasses import Coordinates


class Config:
    def __init__(self):
        self.args = ArgParser().run()
        self.zoom_factor = int(self.args.zoom_factor)
        self.tile_size = int(self.args.tile_size) * self.zoom_factor
        self.offset = Coordinates()

        self.map_data: pytmx.TiledMap
        self.__initialize_pygame()

        self.screen_size = Coordinates(x=int(self.args.screen_width),
                                       y=int(self.args.screen_height))
        self.map_size = Coordinates(x=self.map_data.width * self.tile_size,
                                    y=self.map_data.height * self.tile_size)

        print(f"Screen size: {self.screen_size.x}, {self.screen_size.y}")
        print(f"Map size: {self.map_size.x}, {self.map_size.y}")

        self.character_location = self.args.character_location
        self.character_png_location = self.args.character_png_location
        self.movement_speed = int(self.args.movement_speed)

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.set_spawn_point()
        self.spawn = Coordinates(x=self.rect.x // self.tile_size, y=self.rect.y // self.tile_size)

        self.__surplus = Coordinates()

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.args.screen_width), int(self.args.screen_height)))
        self.map_data = pytmx.load_pygame(self.args.map_location)
        pygame.display.set_caption(title)

    def set_spawn_point(self):
        spawn_obj = next((obj for obj in self.map_data.objects if obj.name == "Spawn"), None)
        if spawn_obj:
            print(spawn_obj.x, spawn_obj.y)

            self.rect.x = (int(spawn_obj.x * self.zoom_factor) // self.tile_size) * self.tile_size
            self.rect.y = (int(spawn_obj.y * self.zoom_factor) // self.tile_size) * self.tile_size

            print(self.rect.x, self.rect.y)

    @property
    def surplus(self):
        return self.__surplus

    def set_surplus(self, axis: str, value: int):
        # Calculate the absolute maximum surplus value allowed
        absolute_max_value = getattr(self.screen_size, axis) // 2

        # Calculate spawn position and determine the maximum surplus value based on the map center
        spawn_x = getattr(self.spawn, axis) * self.tile_size
        max_value = min(spawn_x, getattr(self.map_size, axis) - spawn_x) if spawn_x < self.map_size.x // 2 else getattr(
            self.map_size, axis) - spawn_x

        # Set the surplus value, ensuring it doesn't exceed the absolute maximum
        setattr(self.__surplus, axis, min(min(value, max_value), absolute_max_value))
