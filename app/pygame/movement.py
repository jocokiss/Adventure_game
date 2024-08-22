import pygame


class MovementHandler:
    def __init__(self, config, character):
        self.config = config
        self.character = character

    def __check_collision(self, move_x: int = 0, move_y: int = 0) -> bool:
        new_x, new_y = move_x // self.config.tile_size, move_y // self.config.tile_size

        current_x, current_y = self.character.coordinate.x, self.character.coordinate.y
        if ((current_x + new_x), (current_y + new_y)) in self.config.no_go_zone:
            return True
        return False

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

    def process_movement(self, keys, dt):
        move_x, move_y = 0, 0
        moving = False

        self.config.move_timer += dt

        direction_map = {
            pygame.K_LEFT: ('left', -self.config.tile_size, 0),
            pygame.K_RIGHT: ('right', self.config.tile_size, 0),
            pygame.K_UP: ('up', 0, -self.config.tile_size),
            pygame.K_DOWN: ('down', 0, self.config.tile_size)
        }

        for key, (direction, dx, dy) in direction_map.items():
            if keys[key]:
                moving = True
                if self.config.move_timer >= int(self.config.args.movement_speed):
                    move_x, move_y = dx, dy
                    self.config.move_timer = 0
                self.character.current_direction = direction
                break

        if moving and not self.__check_collision(move_x, move_y):
            self.__adjust_position(move_x, move_y)
            # Handle animation
            self.character.frame_timer += 1
            if self.character.frame_timer >= 7:
                self.character.frame_timer = 0
                self.character.current_frame = (self.character.current_frame + 1) % len(
                    self.character.character_frames[self.character.current_direction]["1"])
        else:
            self.character.current_frame = 0
