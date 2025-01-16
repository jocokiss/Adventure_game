from typing import Optional

import pygame
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    x: int = 0
    y: int = 0


class AnimationFrame(BaseModel):
    image: pygame.Surface = None
    duration: int = 0

    class Config:
        arbitrary_types_allowed = True


class NPCAttributes(BaseModel):
    state: str = "ASLEEP"
    interaction_range: int = 2
    is_stationary: bool = True
    patrol_path: Optional[list[tuple[int, int]]] = Field(default_factory=list)
    current_patrol_index: int = 0
    is_random_movement: bool = False
