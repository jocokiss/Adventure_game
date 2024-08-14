import pygame
import pytmx
import sys

from app.config import Config


class BasicGame:
    def __init__(self):
        self.config = Config()
        
        self.pygame = None
        self.map_data = None
        
        self.collision_rects = []
        self.tiles = {}

        self.__offset_x = None
        self.__offset_y = None
        self.__player_x = None
        self.__player_y = None
        
    def getting_dimensions(self):
        # Calculate map dimensions
        map_width = self.map_data.width * self.config.tile_size
        map_height = self.map_data.height * self.config.tile_size

        # Initial offset for the map (start with the map centered)
        self.__offset_x = (self.config.screen_width - map_width) // 2
        self.__offset_y = (self.config.screen_height - map_height) // 2

        # Position the player in the center of the screen
        self.__player_x = self.config.screen_width // 4 - self.config.tile_size // 2
        self.__player_y = self.config.screen_height // 4 - self.config.tile_size // 2

    def __load_collision_rects(self):
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid == 1:  # Skip empty tiles
                        continue
                    tile_properties = self.map_data.get_tile_properties_by_gid(gid)
                    if tile_properties and 'colliders' in tile_properties:
                        for obj in tile_properties['colliders']:
                            rect_x = x * self.config.tile_size + obj.x
                            rect_y = y * self.config.tile_size + obj.y
                            rect_w = obj.width
                            rect_h = obj.height
                            self.collision_rects.append(pygame.Rect(rect_x, rect_y, rect_w, rect_h))

    def __preload_tiles(self):
        for gid in range(len(self.map_data.images)):
            image = self.map_data.get_tile_image_by_gid(gid)
            if image:
                self.tiles[gid] = image

    def __draw_map(self, x_offset, y_offset):
        # Calculate the range of tiles that are visible on the screen
        start_x = max(0, -x_offset // self.config.tile_size)
        end_x = min(self.map_data.width, (self.config.screen_width - x_offset) // self.config.tile_size + 1)
        start_y = max(0, -y_offset // self.config.tile_size)
        end_y = min(self.map_data.height, (self.config.screen_height - y_offset) // self.config.tile_size + 1)

        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        gid = layer.data[y][x]  # Access the tile GID using separate indices
                        if gid:
                            tile = self.tiles.get(gid)
                            if tile:
                                self.screen.blit(tile, (x * self.config.tile_size + x_offset,
                                                        y * self.config.tile_size + y_offset))

    def check_collision(self, player_rectangle):
        for rect in self.collision_rects:
            if player_rectangle.colliderect(rect):
                return True
        return False
                            
    def __initialize_pygame(self, title: str = "AdventureGame"):
        self.pygame = pygame.init
        self.screen = pygame.display.set_mode(self.config.screen_width, self.config.screen_height)
        self.map_data = pytmx.load_pygame(self.config.map_location)
        pygame.display.set_caption(title)
        
    def run(self):
        self.__initialize_pygame()
        self.__load_collision_rects()
        self.__preload_tiles()

        running = True
        while running:
            for event in self.pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = self.pygame.key.get_pressed()

            # Calculate potential new player position
            new_offset_x = offset_x
            new_offset_y = offset_y

            if keys[pygame.K_LEFT]:
                new_offset_x += self.config.movement_speed
            if keys[pygame.K_RIGHT]:
                new_offset_x -= self.config.movement_speed
            if keys[pygame.K_UP]:
                new_offset_y += self.config.movement_speed
            if keys[pygame.K_DOWN]:
                new_offset_y -= self.config.movement_speed

            # Create a rectangle for the player to check collisions
            player_rect = pygame.Rect(self.__player_x - new_offset_x,
                                      self.__player_y - new_offset_y,
                                      self.config.tile_size,
                                      self.config.tile_size)

            # Move the player if no collision occurs
            if not self.check_collision(player_rect):
                offset_x = new_offset_x
                offset_y = new_offset_y

            # Draw the map with the updated offsets
            self.__draw_map(offset_x, offset_y)

            # draw_collision_borders(offset_x, offset_y)
            # Draw the player (for simplicity, a red square)
            pygame.draw.rect(self.screen, (255, 0, 0), (
                self.__player_x,
                self.__player_y,
                self.config.tile_size,
                self.config.tile_size))

            # Update the display
            self.pygame.display.flip()

            # Frame rate
            self.pygame.time.Clock().tick(60)


# def draw_collision_borders(offset_x, offset_y):
#     for rect in collision_rects:
#         adjusted_rect = pygame.Rect(rect.x + offset_x, rect.y + offset_y, rect.width, rect.height)
#         pygame.draw.rect(screen, (255, 0, 0), adjusted_rect, 2)


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()
