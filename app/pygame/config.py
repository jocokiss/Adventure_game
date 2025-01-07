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
        self.no_go_zone = set()
        self.border_tiles = {}

        self.move_timer = 0
        self.animation_timer = 0

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
        """Preload and scale the tiles for rendering."""
        for gid in range(self.map_data.maxgid):
            tile_properties = self.map_data.get_tile_properties_by_gid(gid)
            image = self.map_data.get_tile_image_by_gid(gid)

            if image:
                if tile_properties and 'Animated' in tile_properties:
                    self.tiles[gid] = [
                        pygame.transform.scale(
                            self.map_data.get_tile_image_by_gid(frame.gid),
                            (self.tile_size, self.tile_size)
                        )
                        for frame in tile_properties['frames']
                    ]
                else:
                    self.tiles[gid] = [pygame.transform.scale(image, (self.tile_size, self.tile_size))]

    def __set_spawn_point(self):
        if spawn_obj := self.get_object("Spawn"):
            self.rect.x = (int(spawn_obj.x * self.zoom_factor) // self.tile_size) * self.tile_size
            self.rect.y = (int(spawn_obj.y * self.zoom_factor) // self.tile_size) * self.tile_size

    def get_object(self, object_name: str):
        return next((obj for obj in self.map_data.objects if obj.name == object_name), None)

    def get_animated_tile(self, gid, dt):
        """Get the current frame of an animated tile based on the accumulated animation timer."""
        if gid in self.tiles and len(self.tiles[gid]) > 1:
            tile_frames = self.tiles[gid]

            # Update the animation timer with dt
            self.animation_timer += dt

            # Determine the frame index based on animation_timer and the number of frames
            frame_index = (self.animation_timer //
                           (int(self.args.movement_speed) * self.zoom_factor)) % len(tile_frames)
            # Return the current frame
            return tile_frames[frame_index]

        # If it's a static tile, return the single frame
        return self.tiles.get(gid)[0]

    def __load_collision_rects(self):
        unreachable_tiles = {"water", "rock"}

        for layer in self.map_data.visible_layers:

            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            for x, y, gid in layer:
                props = self.map_data.get_tile_properties_by_gid(gid) or {}

                if props.get("type") in unreachable_tiles:
                    self.no_go_zone.add((x, y))

                if props.get("border"):
                    borders = {side.strip() for side in props["border"].split(",")}
                    self.border_tiles[(x, y)] = borders

        print(self.border_tiles)

    def __set_coordinates(self):
        self.screen_size.x, self.screen_size.y = int(self.args.screen_width), int(self.args.screen_height)
        self.map_size.x, self.map_size.y = ((self.map_data.width * self.tile_size),
                                            (self.map_data.height * self.tile_size))

        self.map_center.x, self.map_center.y = self.rect.x // self.tile_size, self.rect.y // self.tile_size
