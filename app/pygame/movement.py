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
            setattr(character.body_rect, axis, max(0, new_pos))
        elif offset + screen_size + move >= map_size + self.config.tile_size:
            new_surplus = surplus + abs(move)
            self.config.set_surplus(axis, new_surplus)
            setattr(character.body_rect, axis, min(screen_size - self.config.tile_size, new_pos))
        elif surplus > 0:
            surplus_move = min(abs(move), surplus)
            new_surplus = surplus - surplus_move
            self.config.set_surplus(axis, new_surplus)
            setattr(character.body_rect, axis, new_pos)
        else:
            new_spawn = spawn_value + move // config.tile_size
            setattr(config.spawn, axis, new_spawn)

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
                if self.config.move_timer >= self.config.movement_speed:
                    move_x, move_y = dx, dy
                    self.config.move_timer = 0
                self.character.current_direction = direction
                break

        if moving:
            new_x = self.character.body_rect.x + move_x
            new_y = self.character.body_rect.y + move_y

            if not self.__check_collision(move_x, move_y):
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
