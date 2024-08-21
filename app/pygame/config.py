import pygame
import pytmx

from app.utilities.arg_parser import ArgParser
from app.utilities.dataclasses import Coordinates


class Config:
    def __init__(self):
        self.args = ArgParser().run()
        self.zoom_factor = int(self.args.zoom_factor)
        self.tiles: dict = {}
        self.tile_size = int(self.args.tile_size) * self.zoom_factor
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.no_go_zone = []
        self.move_timer = 0

        self.offset: Coordinates = Coordinates()
        self.__surplus: Coordinates = Coordinates()

        self.map_data: pytmx.TiledMap
        self.__initialize_pygame()

        self.screen_size: Coordinates = Coordinates(x=int(self.args.screen_width),
                                                    y=int(self.args.screen_height))
        self.map_size: Coordinates = Coordinates(x=self.map_data.width * self.tile_size,
                                                 y=self.map_data.height * self.tile_size)

        self.character_png_location = self.args.character_png_location
        self.movement_speed = int(self.args.movement_speed)

        self.spawn = Coordinates(x=self.rect.x // self.tile_size, y=self.rect.y // self.tile_size)

        self.char_coord: Coordinates = Coordinates(x=self.rect.x // self.tile_size, y=self.rect.y // self.tile_size)

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.args.screen_width), int(self.args.screen_height)))
        self.map_data = pytmx.load_pygame(self.args.map_location)
        self.__preload_tiles()
        self.__set_spawn_point()
        self.__load_collision_rects()
        pygame.display.set_caption(title)

    def __preload_tiles(self):
        for gid in range(len(self.map_data.images)):
            image = self.map_data.get_tile_image_by_gid(gid)
            if image:
                scaled_image = pygame.transform.scale(image, (self.tile_size, self.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def __set_spawn_point(self):
        spawn_obj = next((obj for obj in self.map_data.objects if obj.name == "Spawn"), None)
        if spawn_obj:
            self.rect.x = (int(spawn_obj.x * self.zoom_factor) // self.tile_size) * self.tile_size
            self.rect.y = (int(spawn_obj.y * self.zoom_factor) // self.tile_size) * self.tile_size

    def __load_collision_rects(self):
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_properties = self.map_data.get_tile_properties_by_gid(gid)
                    if tile_properties and 'can_reach' in tile_properties:
                        if not tile_properties['can_reach']:
                            self.no_go_zone.append((x, y))

    @property
    def surplus(self):
        return self.__surplus

    def set_surplus(self, axis: str, value: int):
        # Calculate the absolute maximum surplus value allowed
        absolute_max_value = getattr(self.screen_size, axis) // 2

        # Calculate spawn position and determine the maximum surplus value based on the map center
        spawn_x = getattr(self.spawn, axis) * self.tile_size
        max_value = min(spawn_x, getattr(self.map_size, axis) - spawn_x) if spawn_x < self.map_size.x // 2 \
            else getattr(self.map_size, axis) - spawn_x

        # Set the surplus value, ensuring it doesn't exceed the absolute maximum
        setattr(self.__surplus, axis, min(min(value, max_value), absolute_max_value))
