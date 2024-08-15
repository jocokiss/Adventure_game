import pygame
import pytmx
import sys
import xml.etree.ElementTree as ET

from app.config import Config


class BasicGame:
    def __init__(self):
        self.character_data = None
        self.config = Config()

        self.tile_size = self.config.tile_size  # Use the tile size from the config

        self.map_data = None

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
        self.__player_x = tile_x * self.tile_size
        self.__player_y = tile_y * self.tile_size

        # Center the map around the player's position
        self.__offset_x = self.config.screen_width // 2 - self.__player_x - self.tile_size // 2
        self.__offset_y = self.config.screen_height // 2 - self.__player_y - self.tile_size // 2

    def __load_character_from_tiled(self, tsx_file):
        # Parse the .tsx file as XML
        tree = ET.parse(tsx_file)
        root = tree.getroot()

        tile_width = int(root.attrib['tilewidth']) * self.config.zoom_factor
        tile_height = int(root.attrib['tileheight']) * self.config.zoom_factor
        image_width = int(root.find("image").attrib['width'])

        # Load the tileset image
        tileset_image = pygame.image.load(self.config.character_png_location).convert_alpha()

        # Initialize frames storage
        self.character_frames = {
            'down': {
                "1": [],
                "2": []
            },
            'left': {
                "1": [],
                "2": []
            },
            'right': {
                "1": [],
                "2": []
            },
            'up': {
                "1": [],
                "2": []
            },
        }

        # Iterate through each tile element
        for tile in root.findall("tile"):
            properties_element = tile.find('properties')
            if properties_element is not None:
                properties = {prop.attrib['name']: prop.attrib['value'] for prop in
                              properties_element.findall('property')}
                direction = properties.get('Direction')
                part = properties.get('Part')
                if direction and part:
                    # Load the animation frames if the tile has an animation
                    animation_element = tile.find('animation')
                    if animation_element is not None:
                        for frame in animation_element.findall('frame'):
                            frame_tile_id = int(frame.attrib['tileid'])
                            duration = int(frame.attrib['duration'])

                            tile_x = (frame_tile_id % (image_width // (tile_width // self.config.zoom_factor))) * (
                                        tile_width // self.config.zoom_factor)
                            tile_y = (frame_tile_id // (image_width // (tile_width // self.config.zoom_factor))) * (
                                        tile_height // self.config.zoom_factor)
                            tile_image = tileset_image.subsurface(
                                pygame.Rect(tile_x, tile_y, tile_width // self.config.zoom_factor,
                                            tile_height // self.config.zoom_factor))

                            # Scale the tile_image according to the zoom factor
                            scaled_tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

                            # Append the frame to the direction's list
                            self.character_frames[direction][part].append((scaled_tile_image, duration))

        # Combine head and body for each direction
        for direction, parts in self.character_frames.items():
            for part, frames in parts.items():
                if frames:
                    combined_frames = []
                    for frame, duration in frames:
                        combined_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                        combined_surface.blit(frame, (0, 0))
                        combined_frames.append((combined_surface, duration))
                    self.character_frames[direction][part] = combined_frames
                else:
                    print(f"Warning: Missing parts for direction {direction}")
        print(self.character_frames)

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
                scaled_image = pygame.transform.scale(image, (self.tile_size, self.tile_size))  # Scale the tile
                self.tiles[gid] = scaled_image

    def __draw_map(self, offset_x, offset_y):
        # Calculate the range of tiles that are visible on the screen
        start_x = max(0, -offset_x // self.tile_size)
        end_x = min(self.map_data.width, (self.config.screen_width - offset_x) // self.tile_size + 1)
        start_y = max(0, -offset_y // self.tile_size)
        end_y = min(self.map_data.height, (self.config.screen_height - offset_y) // self.tile_size + 1)

        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        gid = layer.data[y][x]  # Access the tile GID using separate indices
                        if gid:
                            tile = self.tiles.get(gid)
                            if tile:
                                self.screen.blit(tile, (x * self.tile_size + offset_x,
                                                        y * self.tile_size + offset_y))

    def check_collision(self, new_offset_x, new_offset_y):
        # Calculate the player's new position on the map based on the proposed offsets
        map_player_x = (self.config.screen_width // 2 - self.tile_size // 2) - new_offset_x
        map_player_y = (self.config.screen_height // 2 - self.tile_size // 2) - new_offset_y

        # Adjust player rectangle according to the zoom factor
        player_rect = pygame.Rect(
            map_player_x,
            map_player_y,
            self.tile_size * self.config.zoom_factor,
            self.tile_size * self.config.zoom_factor
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

    def __update_animation(self, moving):
        # Handle animation for both parts (head and body)
        current_frames_head = self.character_frames[self.current_direction]["1"]
        current_frames_body = self.character_frames[self.current_direction]["2"]

        # Ensure both parts have the same number of frames
        if len(current_frames_head) == len(current_frames_body):
            if moving:
                # Cycle through the frames
                self.frame_timer += 1
                if self.frame_timer >= current_frames_head[self.current_frame][1] // 16:  # Adjust timing as needed
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(current_frames_head)
            else:
                self.current_frame = 0  # If not moving, show the first frame

        # Combine head and body into one surface
        current_head_image = current_frames_head[self.current_frame][0]
        current_body_image = current_frames_body[self.current_frame][0]

        # Adjusted Surface to fit exactly both head and body
        self.combined_surface = pygame.Surface(
            (current_head_image.get_width(), current_head_image.get_height() * 2),
            pygame.SRCALPHA
        )

        # Blit the head at the top of the combined surface
        self.combined_surface.blit(current_head_image, (0, 0))

        # Blit the body directly below the head
        self.combined_surface.blit(current_body_image, (0, current_head_image.get_height()))

    def run(self):
        self.__initialize_pygame()
        self.__set_positions(tile_x=10, tile_y=5)
        self.__load_character_from_tiled(self.config.character_location)
        self.__preload_tiles()  # Load the tiles for drawing the map

        running = True
        move_timer = 0  # Timer to control movement speed

        while running:
            dt = pygame.time.Clock().tick(60)  # Time in milliseconds since the last frame
            move_timer += dt  # Increment the movement timer

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            new_offset_x = self.__offset_x
            new_offset_y = self.__offset_y
            moving = False

            if keys[pygame.K_LEFT]:
                moving = True
                if move_timer >= 200:  # Control the movement speed with a timer
                    new_offset_x += self.tile_size
                    move_timer = 0  # Reset the movement timer
                if self.current_direction != 'left':
                    self.current_frame = 0
                self.current_direction = 'left'
            elif keys[pygame.K_RIGHT]:
                moving = True
                if move_timer >= 200:  # Control the movement speed with a timer
                    new_offset_x -= self.tile_size
                    move_timer = 0  # Reset the movement timer
                if self.current_direction != 'right':
                    self.current_frame = 0
                self.current_direction = 'right'
            elif keys[pygame.K_UP]:
                moving = True
                if move_timer >= 200:  # Control the movement speed with a timer
                    new_offset_y += self.tile_size
                    move_timer = 0  # Reset the movement timer
                if self.current_direction != 'up':
                    self.current_frame = 0
                self.current_direction = 'up'
            elif keys[pygame.K_DOWN]:
                moving = True
                if move_timer >= 200:  # Control the movement speed with a timer
                    new_offset_y -= self.tile_size
                    move_timer = 0  # Reset the movement timer
                if self.current_direction != 'down':
                    self.current_frame = 0
                self.current_direction = 'down'

            if moving:
                # Only update the position if the player is moving and no collision
                if not self.check_collision(new_offset_x, new_offset_y):
                    self.__offset_x = new_offset_x
                    self.__offset_y = new_offset_y

                # Cycle through the frames when moving
                self.frame_timer += 1
                if self.frame_timer >= 8:  # Adjust timing as needed for animation speed
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(
                        self.character_frames[self.current_direction]["1"])
            else:
                # If not moving, reset to the first frame
                self.current_frame = 0

            # Combine head and body into one surface
            current_head_image = self.character_frames[self.current_direction]["1"][self.current_frame][0]
            current_body_image = self.character_frames[self.current_direction]["2"][self.current_frame][0]

            combined_surface = pygame.Surface(
                (current_head_image.get_width(), current_head_image.get_height() * 2),
                pygame.SRCALPHA
            )
            combined_surface.blit(current_head_image, (0, 0))
            combined_surface.blit(current_body_image, (0, current_head_image.get_height()))

            # Draw the map and character
            self.__draw_map(self.__offset_x, self.__offset_y)

            screen_x = self.config.screen_width // 2 - self.tile_size // 2
            screen_y = self.config.screen_height // 2 - self.tile_size // 2
            self.screen.blit(combined_surface, (screen_x, screen_y))

            pygame.display.flip()

if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()