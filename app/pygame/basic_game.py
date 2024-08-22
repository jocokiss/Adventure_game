import pygame
import pytmx
import sys

from app.pygame.config import Config

from app.pygame.character import Sprites
from app.pygame.movement import MovementHandler


class BasicGame:
    def __init__(self):
        self.config = Config()
        self.character = Sprites(self.config)
        self.movement = MovementHandler(self.config, self.character)

    def __draw_map(self, dt: int):
        # Calculate half of the screen width and height in tiles
        half_screen_tiles_x = (self.config.screen_size.x // self.config.tile_size) // 2
        half_screen_tiles_y = (self.config.screen_size.y // self.config.tile_size) // 2

        # Calculate the offsets to center the specific tile
        self.config.offset.x = (self.config.map_center.x * self.config.tile_size) - (self.config.screen_size.x // 2) + (
                self.config.tile_size // 2)
        self.config.offset.y = (self.config.map_center.y * self.config.tile_size) - (self.config.screen_size.y // 2) + (
                self.config.tile_size // 2)

        # Calculate the start and end positions for tiles to draw
        start_x = max(0, self.config.map_center.x - half_screen_tiles_x)
        end_x = min(self.config.map_data.width, self.config.map_center.x + half_screen_tiles_x + 3)
        start_y = max(0, self.config.map_center.y - half_screen_tiles_y)
        end_y = min(self.config.map_data.height, self.config.map_center.y + half_screen_tiles_y + 3)

        for layer in self.config.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.config.get_animated_tile(gid, dt)
                            if tile:
                                # Calculate where to draw the tile on the screen
                                blit_x = (x - start_x) * self.config.tile_size
                                blit_y = (y - start_y) * self.config.tile_size
                                self.config.screen.blit(tile, (blit_x, blit_y))

    def run(self):

        running = True
        while running:
            dt = pygame.time.Clock().tick(60)  # Time in milliseconds since the last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.movement.process_movement(keys, dt)
            self.__draw_map(dt)

            self.character.update()
            self.character.draw(self.config.screen)

            pygame.draw.rect(self.config.screen, (255, 0, 0), self.character.body_rect, 2)

            pygame.display.flip()


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()
