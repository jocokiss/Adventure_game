class CombatAttributes:
    def __init__(self, health=100, mana=50, stamina=50, skills=None):
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.skills = skills or []  # List of Skill objects

        self.current_xp = 10
        self.required_xp = 90
        self.level = 3
        self.max_level = 10

    def take_damage(self, amount):
        """Reduce health when taking damage."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Restore health."""
        self.health += amount

    def add_skill(self, skill):
        """Add a skill to the player's skill list."""
        self.skills.append(skill)