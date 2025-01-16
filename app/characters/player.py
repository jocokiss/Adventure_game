from abc import ABC

from app.sprites.player.player_sprite import PlayerSprite


class Player(ABC):
    def __init__(self, config):
        self.sprite = PlayerSprite(config)  # Handles rendering
        self.combat = CombatAttributes()   # Handles combat

    def use_skill(self, skill_index, target):
        """Use a skill on a target."""
        if 0 <= skill_index < len(self.combat.skills):
            skill = self.combat.skills[skill_index]
            if self.combat.mana >= skill.mana_cost:
                self.combat.mana -= skill.mana_cost
                skill.use(self, target)
                print(f"Used {skill.name} on {target}")
            else:
                print(f"Not enough mana to use {skill.name}!")
        else:
            print("Invalid skill index!")