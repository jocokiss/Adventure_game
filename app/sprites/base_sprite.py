import random
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional

import pygame
import xml.etree.ElementTree as ET

from pydantic import Field

from app.gameplay.config import Config
from app.utilities.dataclasses import Coordinates, AnimationFrame, NPCAttributes
from app.utilities.tiled import Tiled


class BaseSprite(pygame.sprite.Sprite, ABC):
    def __init__(self, config):
        super().__init__()
        self.config: Config = config

        # Initialize the main rect which will represent the body (rect_A)
        self.body_rect = pygame.Rect(0, 0, 0, 0)
        self.head_rect = pygame.Rect(0, 0, 0, 0)

        self.image: Optional[pygame.Surface] = Field(default=None)
        self.state: str = 'WALK'
        self.current_direction: str = "DOWN"
        self.current_frame: int = 0
        self.frame_timer: int = 0
        self.sleep_timer: int = 0
        self.move_timer: int = 0

    @property
    @abstractmethod
    def coordinate(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        """Draw the body and head parts of the sprite on the screen."""
        pass

    @abstractmethod
    def walking_animation(self):
        """Increment frame timers and cycle through animation frames."""
        pass
