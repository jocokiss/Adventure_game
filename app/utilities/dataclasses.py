from typing import Optional, Callable

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


class Skill(BaseModel):
    name: str
    description: str
    damage: Optional[int] = None  # Damage dealt by the skill
    healing: Optional[int] = None  # Healing amount
    resource_cost: Optional[dict] = None  # Resources required, e.g., {"mana": 10}
    effect: Optional[Callable] = None  # Custom effect logic

    def use(self, user, target):
        """
        Apply the skill's effect.
        Args:
            user: The character using the skill.
            target: The character receiving the effect.
        """
        # Check resource costs
        if self.resource_cost:
            for resource, cost in self.resource_cost.items():
                if getattr(user, resource, 0) < cost:
                    print(f"Not enough {resource} to use {self.name}!")
                    return False  # Skill fails if resources are insufficient
                setattr(user, resource, getattr(user, resource) - cost)

        # Apply effects
        if self.damage and target:
            target.take_damage(self.damage)
        if self.healing and user:
            user.heal(self.healing)
        if self.effect:
            self.effect(user, target)  # Apply custom effect logic
        return True
