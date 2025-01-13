import pygame
from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int = 0
    y: int = 0


class AnimationFrame(BaseModel):
    image: pygame.Surface = None
    duration: int = 0

    class Config:
        arbitrary_types_allowed = True
