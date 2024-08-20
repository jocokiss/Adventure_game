import pygame
import pytmx
import sys

from app.pygame.config import Config

from app.pygame.character import Sprites


class BasicGame:
    def __init__(self):
        self.config = Config()
        self.character = Sprites(self.config)

        self.no_go_zone = []
        self.tiles = {}

        self.move_timer = 0

    def __draw_map(self):
        # Calculate half of the screen width and height in tiles
        half_screen_tiles_x = (self.config.screen_size.x // self.config.tile_size) // 2
        half_screen_tiles_y = (self.config.screen_size.y // self.config.tile_size) // 2

        # Calculate the offsets to center the specific tile
        self.config.offset.x = (self.config.spawn.x * self.config.tile_size) - (self.config.screen_size.x // 2) + (
                    self.config.tile_size // 2)
        self.config.offset.y = (self.config.spawn.y * self.config.tile_size) - (self.config.screen_size.y // 2) + (
                    self.config.tile_size // 2)

        # Calculate the start and end positions for tiles to draw
        start_x = max(0, self.config.spawn.x - half_screen_tiles_x)
        end_x = min(self.config.map_data.width, self.config.spawn.x + half_screen_tiles_x + 1)
        start_y = max(0, self.config.spawn.y - half_screen_tiles_y)
        end_y = min(self.config.map_data.height, self.config.spawn.y + half_screen_tiles_y + 1)

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
                            self.no_go_zone.append((x, y))

    def __preload_tiles(self):
        for gid in range(len(self.config.map_data.images)):
            image = self.config.map_data.get_tile_image_by_gid(gid)
            if image:
                scaled_image = pygame.transform.scale(image,
                                                      (self.config.tile_size, self.config.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def check_collision(self):
        if None in self.no_go_zone:
            print("True")
            return True
        return False

    def __process_movement(self, keys, dt):
        move_x, move_y = 0, 0
        moving = False

        self.move_timer += dt

        direction_map = {
            pygame.K_LEFT: ('left', -self.config.tile_size, 0),
            pygame.K_RIGHT: ('right', self.config.tile_size, 0),
            pygame.K_UP: ('up', 0, -self.config.tile_size),
            pygame.K_DOWN: ('down', 0, self.config.tile_size)
        }

        for key, (direction, dx, dy) in direction_map.items():
            if keys[key]:
                moving = True
                if self.move_timer >= self.config.movement_speed:
                    move_x, move_y = dx, dy
                    self.move_timer = 0
                self.character.current_direction = direction
                break

        if moving:
            new_x = self.character.rect.x + move_x
            new_y = self.character.rect.y + move_y

            if not self.check_collision():
                self.__adjust_position(new_x, move_x, 'x')
                self.__adjust_position(new_y, move_y, 'y')

                # Handle animation
                self.character.frame_timer += 1
                if self.character.frame_timer >= 7:
                    self.character.frame_timer = 0
                    self.character.current_frame = (self.character.current_frame + 1) % len(
                        self.character.character_frames[self.character.current_direction]["1"])
            else:
                self.character.current_frame = 0

    def __adjust_position(self, new_pos, move, axis):
        config = self.config
        character = self.character

        offset = getattr(config.offset, axis)
        surplus = getattr(config.surplus, axis)
        screen_size = getattr(config.screen_size, axis)
        map_size = getattr(config.map_size, axis)
        spawn_value = getattr(config.spawn, axis)

        if offset + move <= 0:
            new_surplus = surplus + abs(move)
            self.config.set_surplus(axis, new_surplus)
            setattr(character.rect, axis, max(0, new_pos))
        elif offset + screen_size + move >= map_size:
            new_surplus = surplus + abs(move)
            self.config.set_surplus(axis, new_surplus)
            setattr(character.rect, axis, min(screen_size - self.config.tile_size, new_pos))
        elif surplus > 0:
            surplus_move = min(abs(move), surplus)
            new_surplus = surplus - surplus_move
            self.config.set_surplus(axis, new_surplus)
            setattr(character.rect, axis, new_pos)
        else:
            new_spawn = spawn_value + move // config.tile_size
            setattr(config.spawn, axis, new_spawn)


        # TODO: character coordinates

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
            self.__process_movement(keys, dt)
            self.character.update()
            #print(f"surplus: {self.config.surplus}")
            print(self.character.rect.x, self.character.rect.y)
            #print(self.config.spawn.x, self.config.spawn.y)
            self.__draw_map()

            # Draw the character
            # Blit the character's image onto the screen
            self.config.screen.blit(self.character.image, self.character.rect.topleft)

            pygame.display.flip()


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()