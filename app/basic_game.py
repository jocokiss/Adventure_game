import pygame
import pytmx
import sys

from app.config import Config


class BasicGame:
    def __init__(self):
        self.config = Config()

        self.tile_size = self.config.tile_size  # Use the tile size from the config

        self.map_data = None

        self.collision_rects = []
        self.tiles = {}

        self.__offset_x = None
        self.__offset_y = None
        self.__player_x = None
        self.__player_y = None

        self.move_timer = 0  # Timer to control continuous movement

    def __set_positions(self, tile_x, tile_y):
        # Set the player's position on the map based on the given tile coordinates
        self.__player_x = tile_x * self.tile_size
        self.__player_y = tile_y * self.tile_size

        # Center the map around the player's position
        self.__offset_x = self.config.screen_width // 2 - self.__player_x - self.tile_size // 2
        self.__offset_y = self.config.screen_height // 2 - self.__player_y - self.tile_size // 2

    def __load_collision_rects(self):
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid == 1:  # Skip empty tiles
                        continue
                    tile_properties = self.map_data.get_tile_properties_by_gid(gid)
                    if tile_properties and 'colliders' in tile_properties:
                        for obj in tile_properties['colliders']:
                            rect_x = x * self.config.tile_size + obj.x * self.config.zoom_factor
                            rect_y = y * self.config.tile_size + obj.y * self.config.zoom_factor
                            rect_w = obj.width * self.config.zoom_factor
                            rect_h = obj.height * self.config.zoom_factor
                            self.collision_rects.append(pygame.Rect(rect_x, rect_y, rect_w, rect_h))

    def __preload_tiles(self):
        for gid in range(len(self.map_data.images)):
            image = self.map_data.get_tile_image_by_gid(gid)
            if image:
                scaled_image = pygame.transform.scale(image, (self.tile_size, self.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def __draw_map(self, offset_x, offset_y):
        # Calculate the range of tiles that are visible on the screen
        start_x = max(0, -offset_x // self.tile_size)
        end_x = min(self.map_data.width, (self.config.screen_width - offset_x) // self.tile_size + 1)
        start_y = max(0, -offset_y // self.tile_size)
        end_y = min(self.map_data.height, (self.config.screen_height - offset_y) // self.tile_size + 1)

        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        gid = layer.data[y][x]  # Access the tile GID using separate indices
                        if gid:
                            tile = self.tiles.get(gid)
                            if tile:
                                self.screen.blit(tile, (x * self.tile_size + offset_x,
                                                        y * self.tile_size + offset_y))

    def check_collision(self, new_offset_x, new_offset_y):
        # Adjust player position relative to the new offsets
        player_rect = pygame.Rect(
            (self.__player_x - new_offset_x) + self.tile_size // 2,
            (self.__player_y - new_offset_y) - self.tile_size // 2,
            self.tile_size,
            self.tile_size
        )

        # Check against each collision rectangle
        for rect in self.collision_rects:
            if player_rect.colliderect(rect):
                return True
        return False

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.map_data = pytmx.load_pygame(self.config.map_location)
        pygame.display.set_caption(title)

    def run(self):
        self.__initialize_pygame()
        self.__set_positions(tile_x=10, tile_y=5)
        self.__load_collision_rects()
        self.__preload_tiles()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if self.move_timer == 0:  # Allow movement only if the timer has reset
                new_offset_x = self.__offset_x
                new_offset_y = self.__offset_y

                if keys[pygame.K_LEFT]:
                    new_offset_x += self.tile_size
                elif keys[pygame.K_RIGHT]:
                    new_offset_x -= self.tile_size
                elif keys[pygame.K_UP]:
                    new_offset_y += self.tile_size
                elif keys[pygame.K_DOWN]:
                    new_offset_y -= self.tile_size

                # Check collision with updated player position
                if not self.check_collision(new_offset_x, new_offset_y):
                    self.__offset_x = new_offset_x
                    self.__offset_y = new_offset_y
                    self.move_timer = self.config.movement_speed  # Delay before the next movement

            # Decrease the movement timer to allow continuous movement
            if self.move_timer > 0:
                self.move_timer -= 1

            self.__draw_map(self.__offset_x, self.__offset_y)

            pygame.draw.rect(self.screen, (255, 0, 0), (
                self.config.screen_width // 2 - self.tile_size // 2,
                self.config.screen_height // 2 - self.tile_size // 2,
                self.tile_size,
                self.tile_size))

            pygame.display.flip()
            pygame.time.Clock().tick(60)


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()