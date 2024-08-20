import pygame


class MovementHandler:
    def __init__(self, config, character, offsets):
        self.config = config
        self.character = character
        self.__offset_x, self.__offset_y = offsets

        self.move_timer = 0
        self.x_surplus = 0
        self.y_surplus = 0

    def check_collision(self):
        pass
        # if None in self.no_go_zone:
        #     print("True")
        #     return True
        # return False

    def process_movement(self, keys, dt):
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
                self.move_along_axis(new_x, move_x, 'x')
                self.move_along_axis(new_y, move_y, 'y')

                # Handle animation
                self.character.frame_timer += 1
                if self.character.frame_timer >= 8:
                    self.character.frame_timer = 0
                    self.character.current_frame = (self.character.current_frame + 1) % len(
                        self.character.character_frames[self.character.current_direction]["1"])
            else:
                self.character.current_frame = 0

    def adjust_position(self, new_pos, move, axis_data):
        offset = axis_data['offset']
        surplus_attr = axis_data['surplus']
        rect_attr = axis_data['rect_attr']
        spawn_attr = axis_data['spawn_attr']
        screen_size_attr = axis_data['screen_size_attr']
        map_size_attr = axis_data['map_size_attr']

        screen_size = getattr(self.config, screen_size_attr)
        map_size = getattr(self.config, map_size_attr)

        if offset + move <= 0:
            setattr(self, surplus_attr, getattr(self, surplus_attr) + abs(move))
            setattr(self.character.rect, rect_attr, max(0, new_pos))
        elif offset + screen_size + move >= map_size:
            setattr(self, surplus_attr, getattr(self, surplus_attr) + abs(move))
            setattr(self.character.rect, rect_attr,
                    min(screen_size - getattr(self.character.rect, f"{rect_attr}_size"), new_pos))
        elif getattr(self, surplus_attr) > 0:
            surplus_move = min(abs(move), getattr(self, surplus_attr))
            setattr(self, surplus_attr, getattr(self, surplus_attr) - surplus_move)
            setattr(self.character.rect, rect_attr, new_pos)
        else:
            setattr(self.config, spawn_attr, getattr(self.config, spawn_attr) + move // self.config.tile_size)

    def move_along_axis(self, new_pos, move, axis):
        axis_data = {
            'x': {
                'offset': self.__offset_x,
                'surplus': 'x_surplus',
                'rect_attr': 'x',
                'spawn_attr': 'spawn_x',
                'screen_size_attr': 'screen_width',
                'map_size_attr': 'map_width',
            },
            'y': {
                'offset': self.__offset_y,
                'surplus': 'y_surplus',
                'rect_attr': 'y',
                'spawn_attr': 'spawn_y',
                'screen_size_attr': 'screen_height',
                'map_size_attr': 'map_height',
            }
        }

        self.adjust_position(new_pos, move, axis_data[axis])

    def get_offsets(self):
        return self.__offset_x, self.__offset_y