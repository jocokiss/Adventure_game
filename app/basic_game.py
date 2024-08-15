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

        # Get the image source and tile size information
        image_source = root.find("image").attrib['source']
        tile_width = int(root.attrib['tilewidth']) * self.config.zoom_factor
        tile_height = int(root.attrib['tileheight']) * self.config.zoom_factor
        image_width = int(root.find("image").attrib['width'])
        image_height = int(root.find("image").attrib['height'])

        # Load the tileset image
        tileset_image = pygame.image.load(self.config.character_png_location).convert_alpha()

        # Initialize frames storage
        self.character_frames = {
            'down': [],
            'left': [],
            'right': [],
            'up': [],
        }

        # Iterate through each tile element
        for tile in root.findall("tile"):
            tile_id = int(tile.attrib['id'])
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
                            self.character_frames[direction].append((scaled_tile_image, duration))

                    else:
                        # Handle non-animated tiles (static frames)
                        tile_x = (tile_id % (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_width // self.config.zoom_factor)
                        tile_y = (tile_id // (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_height // self.config.zoom_factor)
                        tile_image = tileset_image.subsurface(
                            pygame.Rect(tile_x, tile_y, tile_width // self.config.zoom_factor,
                                        tile_height // self.config.zoom_factor))

                        # Scale the tile_image according to the zoom factor
                        scaled_tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

                        self.character_frames[direction].append((scaled_tile_image, 100))  # Assume a default duration

        # Combine head and body for each direction
        for direction, frames in self.character_frames.items():
            if frames:
                combined_frames = []
                for frame, duration in frames:
                    combined_surface = pygame.Surface((tile_width, tile_height * 2), pygame.SRCALPHA)
                    combined_surface.blit(frame, (0, 0))
                    combined_frames.append((combined_surface, duration))
                self.character_frames[direction] = combined_frames
            else:
                print(f"Warning: Missing parts for direction {direction}")

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

    def run(self):
        self.__initialize_pygame()
        self.__set_positions(tile_x=10, tile_y=5)
        self.__load_character_from_tiled(self.config.character_location)  # Replace with the actual path
        self.__preload_tiles()  # Load the tiles for drawing the map

        running = True
        elapsed_time = 0  # Track the elapsed time for animation

        while running:
            dt = pygame.time.Clock().tick(60)  # Time in milliseconds since last frame
            elapsed_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if self.move_timer == 0:
                new_offset_x = self.__offset_x
                new_offset_y = self.__offset_y

                if keys[pygame.K_LEFT]:
                    new_offset_x += self.tile_size
                    self.current_direction = 'left'
                elif keys[pygame.K_RIGHT]:
                    new_offset_x -= self.tile_size
                    self.current_direction = 'right'
                elif keys[pygame.K_UP]:
                    new_offset_y += self.tile_size
                    self.current_direction = 'up'
                elif keys[pygame.K_DOWN]:
                    new_offset_y -= self.tile_size
                    self.current_direction = 'down'

                if not self.check_collision(new_offset_x, new_offset_y):
                    self.__offset_x = new_offset_x
                    self.__offset_y = new_offset_y
                    self.move_timer = self.config.movement_speed

            if self.move_timer > 0:
                self.move_timer -= 1

            # Animation: Switch frames based on elapsed time
            current_frames = self.character_frames[self.current_direction]
            total_duration = sum(frame[1] for frame in current_frames)
            current_time = elapsed_time % total_duration

            frame_index = 0
            accumulated_time = 0

            for frame, duration in current_frames:
                accumulated_time += duration
                if current_time <= accumulated_time:
                    break
                frame_index += 1

            # Extract the surface (image) from the tuple before blitting
            current_frame_image = current_frames[frame_index][0]

            self.__draw_map(self.__offset_x, self.__offset_y)  # Ensure map is drawn

            screen_x = self.config.screen_width // 2 - self.tile_size // 2
            screen_y = self.config.screen_height // 2 - self.tile_size // 2
            self.screen.blit(current_frame_image, (screen_x, screen_y))

            pygame.display.flip()

if __name__ == "__main__":
    pipeline = BasicGame()
    pipeline.run()