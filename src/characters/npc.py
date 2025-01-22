from abc import ABC

from src.gameplay.combat.combat_attr import CombatAttributes
from src.sprites.npc.npc_sprites import NPCSprite


class NPC(ABC):
    def __init__(self, config, initial_position):
        self.name = "Tree-trunk"
        self.sprite = NPCSprite(config, initial_position)  # Handles rendering
        self.combat = CombatAttributes()  # Handles combat
