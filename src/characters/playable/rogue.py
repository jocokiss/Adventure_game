from src.characters.character import Character
from src.utilities.dataclasses import Skill

fireball = Skill(
    name="Fireball",
    damage=30,
    mana_cost=10,
    description="Launch a fiery ball that burns your enemy."
)

heal = Skill(
    name="Heal",
    healing=20,  # Negative damage indicates healing
    mana_cost=15,
    description="Heal yourself or an ally."
)

slash = Skill(
    name="Slash",
    damage=10,
    mana_cost=0,  # No mana cost for basic attacks
    description="A basic melee attack."
)

stun = Skill(
    name="Stun",
    damage=5,
    mana_cost=5,
    description="A light attack that stuns the enemy temporarily."
)


class Rogue(Character):
    def __init__(self, config):
        super().__init__(config)
        self.combat.skills = [fireball, heal, slash, stun]
        self.gold = "12"
