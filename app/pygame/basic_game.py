import pygame
import pytmx
import sys

from app.pygame.config import Config

from app.pygame.character import Sprites
from app.pygame.map import Map
from app.pygame.movement import MovementHandler


class BasicGame:
    def __init__(self):
        self.config = Config()
        self.character = Sprites(self.config)
        self.movement = MovementHandler(self.config, self.character)
        self.map = Map(self.config)

    def run(self):

        running = True
        while running:
            # dt = pygame.time.Clock().tick(60)  # Time in milliseconds since the last frame
            self.config.dt = pygame.time.Clock().tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.movement.process_movement(keys)
            self.config.calculate_offsets()

            self.map.render_background()

            self.character.update()
            self.character.draw()

            self.map.render_foreground()

            pygame.display.flip()


if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()
