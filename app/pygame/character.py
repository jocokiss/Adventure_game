import pygame
import xml.etree.ElementTree as ET


class Sprites(pygame.sprite.Sprite):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.character_frames = None
        self.image = None
        self.current_direction = "down"
        self.current_frame = 0
        self.frame_timer = 0
        self.move_timer = 0

        # Load character frames
        self.load_character_from_tiled()

        # Initialize rect position based on the loaded image size
        self.rect.size = self.image.get_size()
        self.rect.center = (config.screen_width // 2, config.screen_height // 2)

    def load_character_from_tiled(self):
        # Parse the .tsx file as XML
        tree = ET.parse(self.config.character_location)
        root = tree.getroot()

        tile_width = int(root.attrib['tilewidth']) * self.config.zoom_factor
        tile_height = int(root.attrib['tileheight']) * self.config.zoom_factor
        image_width = int(root.find("image").attrib['width'])

        # Load the tileset image
        tileset_image = pygame.image.load(self.config.character_png_location).convert_alpha()

        # Initialize frames storage
        self.character_frames = {
            'down': {"1": [], "2": []},
            'left': {"1": [], "2": []},
            'right': {"1": [], "2": []},
            'up': {"1": [], "2": []},
        }

        # Iterate through each tile element in the .tsx file
        for tile in root.findall("tile"):
            properties_element = tile.find('properties')
            if properties_element is not None:
                properties = {prop.attrib['name']: prop.attrib['value'] for prop in properties_element.findall('property')}
                direction = properties.get('Direction')
                part = properties.get('Part')

                if direction and part:
                    animation_element = tile.find('animation')
                    if animation_element is not None:
                        # Iterate through each frame in the animation
                        for frame in animation_element.findall('frame'):
                            frame_tile_id = int(frame.attrib['tileid'])
                            duration = int(frame.attrib['duration'])

                            # Calculate the position of the tile in the tileset image
                            tile_x = (frame_tile_id % (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_width // self.config.zoom_factor)
                            tile_y = (frame_tile_id // (image_width // (tile_width // self.config.zoom_factor))) * (
                                    tile_height // self.config.zoom_factor)

                            # Extract and scale the tile image
                            tile_image = tileset_image.subsurface(
                                pygame.Rect(tile_x, tile_y, tile_width // self.config.zoom_factor, tile_height // self.config.zoom_factor)
                            )
                            scaled_tile_image = pygame.transform.scale(tile_image, (tile_width, tile_height))

                            # Append the frame to the appropriate direction and part
                            self.character_frames[direction][part].append((scaled_tile_image, duration))

        # Initialize the first frame of the character
        self.update_image()

    def update_image(self):
        # Combine head and body for the current frame and direction
        current_head_image = self.character_frames[self.current_direction]["1"][self.current_frame][0]
        current_body_image = self.character_frames[self.current_direction]["2"][self.current_frame][0]

        self.image = pygame.Surface(
            (current_head_image.get_width(), current_head_image.get_height() * 2),
            pygame.SRCALPHA
        )
        self.image.blit(current_head_image, (0, 0))
        self.image.blit(current_body_image, (0, current_head_image.get_height()))

        # Update the rect size based on the combined image
        self.rect.size = self.image.get_size()

    def update(self, keys, dt):
        # Increment the move timer
        self.move_timer += dt

        # Handle movement and direction
        move_x, move_y = 0, 0
        moving = False

        if keys[pygame.K_LEFT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_x = -self.config.tile_size
                self.move_timer = 0
            self.current_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_x = self.config.tile_size
                self.move_timer = 0
            self.current_direction = 'right'
        elif keys[pygame.K_UP]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_y = -self.config.tile_size
                self.move_timer = 0
            self.current_direction = 'up'
        elif keys[pygame.K_DOWN]:
            moving = True
            if self.move_timer >= self.config.movement_speed:
                move_y = self.config.tile_size
                self.move_timer = 0
            self.current_direction = 'down'

        # Move the character's rect (this moves the camera)
        if moving:
            self.rect.x += move_x
            self.rect.y += move_y

            # Handle animation
            self.frame_timer += 1
            if self.frame_timer >= 8:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.character_frames[self.current_direction]["1"])
        else:
            # Reset to the first frame if not moving
            self.current_frame = 0

        # Update the character's image to the current frame
        self.update_image()
