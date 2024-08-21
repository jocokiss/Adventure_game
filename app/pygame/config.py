import pygame
import pytmx

from app.utilities.arg_parser import ArgParser
from app.utilities.dataclasses import Coordinates


class Config:
    def __init__(self):
        self.args = ArgParser().run()

        self.zoom_factor = int(self.args.zoom_factor)
        self.tile_size = int(self.args.tile_size) * self.zoom_factor

        self.tiles: dict = {}

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.no_go_zone = []
        self.move_timer = 0

        self.offset: Coordinates = Coordinates()
        self.screen_size: Coordinates = Coordinates()
        self.map_size: Coordinates = Coordinates()
        self.map_center: Coordinates = Coordinates()

        self.map_data: pytmx.TiledMap
        self.__initialize_pygame()

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.args.screen_width), int(self.args.screen_height)))
        self.map_data = pytmx.load_pygame(self.args.map_location)
        self.__set_spawn_point()
        self.__set_coordinates()
        self.__preload_tiles()
        self.__load_collision_rects()
        pygame.display.set_caption(title)

    def __preload_tiles(self):
        for gid in range(len(self.map_data.images)):
            image = self.map_data.get_tile_image_by_gid(gid)
            if image:
                scaled_image = pygame.transform.scale(image, (self.tile_size, self.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def __set_spawn_point(self):
        if spawn_obj := self.get_object("Spawn"):
            self.rect.x = (int(spawn_obj.x * self.zoom_factor) // self.tile_size) * self.tile_size
            self.rect.y = (int(spawn_obj.y * self.zoom_factor) // self.tile_size) * self.tile_size

    def get_object(self, object_name: str):
        return next((obj for obj in self.map_data.objects if obj.name == object_name), None)

    def __load_collision_rects(self):
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_properties = self.map_data.get_tile_properties_by_gid(gid)
                    if tile_properties and 'can_reach' in tile_properties:
                        if not tile_properties['can_reach']:
                            self.no_go_zone.append((x, y))

    def __set_coordinates(self):
        self.screen_size.x, self.screen_size.y = int(self.args.screen_width), int(self.args.screen_height)
        self.map_size.x, self.map_size.y = ((self.map_data.width * self.tile_size),
                                            (self.map_data.height * self.tile_size))

        self.map_center.x, self.map_center.y = self.rect.x // self.tile_size, self.rect.y // self.tile_size
