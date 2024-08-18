import pygame
import pytmx

from app.utilities.arg_parser import ArgParser


class Config:
    def __init__(self):
        self.args = ArgParser().run()
        self.zoom_factor = int(self.args.zoom_factor)

        self.map_data = None
        self.__initialize_pygame()

        self.screen_width = int(self.args.screen_width)
        self.screen_height = int(self.args.screen_height)

        self.tile_size = int(self.args.tile_size) * self.zoom_factor
        self.map_location = self.args.map_location
        self.character_location = self.args.character_location
        self.character_png_location = self.args.character_png_location
        self.movement_speed = int(self.args.movement_speed)

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.spawn_x, self.spawn_y = self.set_spawn_point()

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.args.screen_width), int(self.args.screen_height)))
        self.map_data = pytmx.load_pygame(self.args.map_location)
        pygame.display.set_caption(title)

    @property
    def screen_x(self):
        return self.screen_width // 16

    @property
    def screen_y(self):
        return self.screen_height // 16

    def set_spawn_point(self):
        spawn_obj = next((obj for obj in self.map_data.objects if obj.name == "Spawn"), None)
        if spawn_obj:
            # Position the character at the spawn point (centered on the tile)
            self.rect.x = int(spawn_obj.x * self.zoom_factor)
            self.rect.y = int(spawn_obj.y * self.zoom_factor)

            # Center the character on the tile
            self.rect.x = (self.rect.x // self.tile_size) * self.tile_size
            self.rect.y = (self.rect.y // self.tile_size) * self.tile_size

            return self.rect.x // self.tile_size, self.rect.y // self.tile_size
