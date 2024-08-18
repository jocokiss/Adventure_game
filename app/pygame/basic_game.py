import pygame
import pytmx
import sys

from app.pygame.config import Config

from app.pygame.character import Sprites


class BasicGame:
    def __init__(self):
        self.x_surplus = 0
        self.y_surplus = 0

        self.config = Config()
        self.character = Sprites(self.config)

        self.__offset_x = 0
        self.__offset_y = 0
        self.__player_x = 0
        self.__player_y = 0

        self.no_go_zone = []
        self.tiles = {}

        self.move_timer = 0

    def __draw_map(self):
        # Calculate half of the screen width and height in tiles
        half_screen_tiles_x = (self.config.screen_width // self.config.tile_size) // 2
        half_screen_tiles_y = (self.config.screen_height // self.config.tile_size) // 2

        # Calculate the offsets to center the specific tile
        self.__offset_x = (self.config.spawn_x * self.config.tile_size) - (self.config.screen_width // 2) + (
                    self.config.tile_size // 2)
        self.__offset_y = (self.config.spawn_y * self.config.tile_size) - (self.config.screen_height // 2) + (
                    self.config.tile_size // 2)

        # Calculate the start and end positions for tiles to draw
        start_x = max(0, self.config.spawn_x - half_screen_tiles_x)
        end_x = min(self.config.map_data.width, self.config.spawn_x + half_screen_tiles_x + 1)
        start_y = max(0, self.config.spawn_y - half_screen_tiles_y)
        end_y = min(self.config.map_data.height, self.config.spawn_y + half_screen_tiles_y + 1)

        for layer in self.config.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.tiles.get(gid)
                            if tile:
                                # Calculate where to draw the tile on the screen
                                blit_x = (x - start_x) * self.config.tile_size
                                blit_y = (y - start_y) * self.config.tile_size
                                self.config.screen.blit(tile, (blit_x, blit_y))
    def __load_collision_rects(self):
        for layer in self.config.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_properties = self.config.map_data.get_tile_properties_by_gid(gid)
                    if tile_properties and 'can_reach' in tile_properties:
                        if not tile_properties['can_reach']:
                            rect_x = x * self.config.tile_size
                            rect_y = y * self.config.tile_size
                            self.no_go_zone.append((rect_x, rect_y))

    def __preload_tiles(self):
        for gid in range(len(self.config.map_data.images)):
            image = self.config.map_data.get_tile_image_by_gid(gid)
            if image:
                scaled_image = pygame.transform.scale(image,
                                                      (self.config.tile_size, self.config.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def check_collision(self):
        # Calculate the player's new position on the map based on the proposed offsets
        if None in self.no_go_zone:
            print("True")
            return True
        return False

    def __handle_movement(self, keys, dt):
        move_x, move_y = 0, 0
        moving = False

        self.move_timer += dt

        if keys[pygame.K_LEFT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_x = -self.config.tile_size
                self.move_timer = 0
            self.character.current_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_x = self.config.tile_size
                self.move_timer = 0
            self.character.current_direction = 'right'
        elif keys[pygame.K_UP]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_y = -self.config.tile_size
                self.move_timer = 0
            self.character.current_direction = 'up'
        elif keys[pygame.K_DOWN]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_y = self.config.tile_size
                self.move_timer = 0
            self.character.current_direction = 'down'

        if moving:
            new_x = self.character.rect.x + move_x
            new_y = self.character.rect.y + move_y

            if not self.check_collision():
                map_width = self.config.map_data.width * self.config.tile_size
                map_height = self.config.map_data.height * self.config.tile_size

                # Update map offsets and character position based on the map edges
                if self.__offset_x + move_x <= 0:  # Reached left edge
                    self.x_surplus += abs(move_x)  # Increment surplus by the absolute value of move_x
                    self.character.rect.x = max(0, new_x)
                elif self.__offset_x + self.config.screen_width + move_x >= map_width:  # Reached right edge
                    self.x_surplus += abs(move_x)  # Increment surplus by the absolute value of move_x
                    self.character.rect.x = min(self.config.screen_width - self.character.rect.width, new_x)
                elif self.x_surplus > 0:  # Moving in the opposite direction while surplus exists
                    surplus_move = min(abs(move_x), self.x_surplus)  # Determine how much surplus to reduce
                    self.x_surplus -= surplus_move  # Decrease the surplus
                    self.character.rect.x = new_x
                else:  # Normal movement, update spawn_x
                    self.config.spawn_x += move_x // self.config.tile_size

                if self.__offset_y + move_y <= 0:  # Reached top edge
                    self.character.rect.y = max(0, new_y)
                elif self.__offset_y + self.config.screen_height + move_y >= map_height:  # Reached bottom edge
                    self.character.rect.y = min(self.config.screen_height - self.character.rect.height, new_y)
                else:
                    self.config.spawn_y += move_y // self.config.tile_size

                # Handle animation
                self.character.frame_timer += 1
                if self.character.frame_timer >= 8:
                    self.character.frame_timer = 0
                    self.character.current_frame = (self.character.current_frame + 1) % len(
                        self.character.character_frames[self.character.current_direction]["1"])
            else:
                self.character.current_frame = 0

    def run(self):
        self.__preload_tiles()
        self.__load_collision_rects()

        running = True

        while running:
            dt = pygame.time.Clock().tick(60)  # Time in milliseconds since the last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.__handle_movement(keys, dt)
            self.character.update()
            print(self.x_surplus)
            print(self.config.spawn_x, self.config.spawn_y)
            self.__draw_map()

            # Draw the character
            self.config.screen.blit(self.character.image, self.character.rect.topleft)

            pygame.display.flip()


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()