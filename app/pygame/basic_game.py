import pygame
import pytmx
import sys

from app.pygame.config import Config

from app.pygame.character import Sprites


class BasicGame:
    def __init__(self):
        self.config = Config()

        self.all_sprites = pygame.sprite.Group()

        self.map_data = None
        self.__initialize_pygame()
        self.character = Sprites(self.config)
        self.all_sprites.add(self.character)

        self.collision_rects = []
        self.tiles = {}

        self.__offset_x = None
        self.__offset_y = None
        self.__player_x = None
        self.__player_y = None

        self.move_timer = 0  # Timer to control continuous movement
        self.current_direction = "down"
        self.current_frame = 0
        self.frame_timer = 0
        self.frames_per_direction = 4

        self.animations = {}
        self.direction_to_gid = {}  # Dictionary to map directions to starting GIDs

    def __set_positions(self, tile_x, tile_y):
        # Set the player's position on the map based on the given tile coordinates
        self.__player_x = tile_x * self.config.tile_size
        self.__player_y = tile_y * self.config.tile_size

        # Center the map around the player's position
        self.__offset_x = self.config.screen_width // 2 - self.__player_x - self.config.tile_size // 2
        self.__offset_y = self.config.screen_height // 2 - self.__player_y - self.config.tile_size // 2

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
                scaled_image = pygame.transform.scale(image, (self.config.tile_size, self.config.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def __draw_map(self, offset_x, offset_y):
        # Calculate the range of tiles that are visible on the screen
        start_x = max(0, -offset_x // self.config.tile_size)
        end_x = min(self.map_data.width, (self.config.screen_width - offset_x) // self.config.tile_size + 1)
        start_y = max(0, -offset_y // self.config.tile_size)
        end_y = min(self.map_data.height, (self.config.screen_height - offset_y) // self.config.tile_size + 1)

        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        gid = layer.data[y][x]  # Access the tile GID using separate indices
                        if gid:
                            tile = self.tiles.get(gid)
                            if tile:
                                self.screen.blit(tile, (x * self.config.tile_size + offset_x,
                                                        y * self.config.tile_size + offset_y))

    def check_collision(self, new_offset_x, new_offset_y):
        # Calculate the player's new position on the map based on the proposed offsets
        map_player_x = (self.config.screen_width // 2 - self.config.tile_size // 2) - new_offset_x
        map_player_y = (self.config.screen_height // 2 - self.config.tile_size // 2) - new_offset_y

        # Adjust player rectangle according to the zoom factor
        player_rect = pygame.Rect(
            map_player_x,
            map_player_y,
            self.config.tile_size * self.config.zoom_factor,
            self.config.tile_size * self.config.zoom_factor
        )

        # Check collision with all collision rectangles
        for rect in self.collision_rects:
            if player_rect.colliderect(rect):
                return True
        return False

    def __initialize_pygame(self, title: str = "AdventureGame"):
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        self.map_data = pytmx.load_pygame(self.config.map_location)
        pygame.display.set_caption(title)

    def __handle_movement(self, keys):
        new_offset_x = self.__offset_x
        new_offset_y = self.__offset_y
        moving = False

        if keys[pygame.K_LEFT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:  # Control the movement speed with a timer
                new_offset_x += self.config.tile_size
                self.move_timer = 0  # Reset the movement timer
            if self.current_direction != 'left':
                self.current_frame = 0
            self.current_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:  # Control the movement speed with a timer
                new_offset_x -= self.config.tile_size
                self.move_timer = 0  # Reset the movement timer
            if self.current_direction != 'right':
                self.current_frame = 0
            self.current_direction = 'right'
        elif keys[pygame.K_UP]:
            moving = True
            if self.move_timer >= self.config.movement_speed:  # Control the movement speed with a timer
                new_offset_y += self.config.tile_size
                self.move_timer = 0  # Reset the movement timer
            if self.current_direction != 'up':
                self.current_frame = 0
            self.current_direction = 'up'
        elif keys[pygame.K_DOWN]:
            moving = True
            if self.move_timer >= self.config.movement_speed:  # Control the movement speed with a timer
                new_offset_y -= self.config.tile_size
                self.move_timer = 0  # Reset the movement timer
            if self.current_direction != 'down':
                self.current_frame = 0
            self.current_direction = 'down'

        if moving and not self.check_collision(new_offset_x, new_offset_y):
            self.__offset_x = new_offset_x
            self.__offset_y = new_offset_y

    def run(self):
        self.__initialize_pygame()
        self.__set_positions(tile_x=10, tile_y=5)
        self.character = Sprites(self.config)
        self.__preload_tiles()  # Load the tiles for drawing the map

        running = True

        while running:
            dt = pygame.time.Clock().tick(60)  # Time in milliseconds since the last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            self.character.update(keys, dt)
            self.__draw_map(self.__offset_x, self.__offset_y)

            # Draw the character
            self.screen.blit(self.character.image, self.character.rect.topleft)

            pygame.display.flip()


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()