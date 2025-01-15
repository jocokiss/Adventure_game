import pygame

from app.utilities.constants import OPPOSITE_DIRECTION


class MovementHandler:
    def __init__(self, config, character):
        self.config = config
        self.character = character

    def tile_has_border(self, tile_position, direction):
        """Return True if tile at tile_position has a border in the given direction."""
        return (
                tile_position in self.config.border_tiles
                and direction in self.config.border_tiles[tile_position]
        )

    def __check_collision(self, move_x: int = 0, move_y: int = 0) -> bool:
        current_position = (self.character.coordinate.x, self.character.coordinate.y)
        future_position = (
            current_position[0] + move_x // self.config.tile_size,
            current_position[1] + move_y // self.config.tile_size
        )

        facing_direction = self.character.current_direction
        opposite_direction = OPPOSITE_DIRECTION[facing_direction]

        return (
                self.tile_has_border(current_position, facing_direction) or
                self.tile_has_border(future_position, opposite_direction) or
                future_position in self.config.no_go_zone
        )

    def __adjust_position(self, x, y):

        for move in x, y:
            axis = "x" if x else "y"
            new_coord = getattr(self.character.body_rect, axis) + move

            offset = getattr(self.config.offset, axis)
            screen_size = getattr(self.config.screen_size, axis)
            map_size = getattr(self.config.map_size, axis)
            map_center = getattr(self.config.map_center, axis)

            negative_border, positive_border = 0, ((map_size // self.config.tile_size) - 1)
            char_coord = getattr(self.character.coordinate, axis)

            if (char_coord == negative_border and move < 0) or (char_coord == positive_border and move > 0):
                return

            if offset + move <= 0:
                setattr(self.character.body_rect, axis, max(0, new_coord))
            elif offset + screen_size + move >= map_size + self.config.tile_size:
                setattr(self.character.body_rect, axis, min(screen_size - self.config.tile_size, new_coord))
            elif (char_coord / map_center) != 1:
                setattr(self.character.body_rect, axis, new_coord)
            else:
                setattr(self.config.map_center, axis, map_center + move // self.config.tile_size)

    def process_movement(self, keys):
        move_x, move_y = 0, 0
        moving = False

        self.config.move_timer += self.config.dt

        direction_map = {
            pygame.K_LEFT: ('LEFT', -self.config.tile_size, 0),
            pygame.K_RIGHT: ('RIGHT', self.config.tile_size, 0),
            pygame.K_UP: ('UP', 0, -self.config.tile_size),
            pygame.K_DOWN: ('DOWN', 0, self.config.tile_size)
        }

        for key, (direction, dx, dy) in direction_map.items():
            if keys[key]:
                moving = True
                if self.config.move_timer >= int(self.config.args.movement_speed):
                    move_x, move_y = dx, dy
                    self.config.move_timer = 0
                self.character.current_direction = direction
                break

        if moving:
            if not self.__check_collision(move_x, move_y):
                self.__adjust_position(move_x, move_y)
            self.character.walking_animation()

        else:
            # No movement key is pressed; reset animation
            self.character.current_frame = 0
