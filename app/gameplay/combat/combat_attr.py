class CombatAttributes:
    def __init__(self, health=100, mana=50, stamina=50, skills=None):
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.skills = skills or []  # List of Skill objects

    def take_damage(self, amount):
        """Reduce health when taking damage."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Player takes {amount} damage! Remaining health: {self.health}")

    def heal(self, amount):
        """Restore health."""
        self.health += amount
        print(f"Player heals for {amount}! Current health: {self.health}")

    def add_skill(self, skill):
        """Add a skill to the player's skill list."""
        self.skills.append(skill)