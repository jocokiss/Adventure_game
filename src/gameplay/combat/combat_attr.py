from src.utilities.common_utils import calculate_required_xp


class CombatAttributes:
    def __init__(self, health=100, mana=50, stamina=50, skills=None):
        self.level = 1
        self.max_level = 20

        self.max_health = health
        self.health = health

        self.mana = mana

        self.stamina = stamina

        self.skills = skills or []  # List of Skill objects

        self.current_xp = 0
        self.required_xp = calculate_required_xp(self.level)

    @property
    def health_percentage(self):
        return int(self.health / self.max_health * 100)

    @property
    def xp_percentage(self):
        return int(self.current_xp / self.required_xp * 100)

    def gain_xp(self, amount):
        """Handle gaining XP and leveling up."""
        self.current_xp += amount

    def level_up(self):
        """Manually level up and save excess XP."""
        if self.level >= self.max_level:
            print("Already at max level!")
            return

        if self.current_xp < self.required_xp:
            print(f"Not enough XP to level up! Current XP: {self.current_xp}/{self.required_xp}")
            return

        # Deduct the required XP for this level
        self.current_xp -= self.required_xp
        self.level += 1

        if self.level < self.max_level:
            # Update the required XP for the next level
            self.required_xp = self.calculate_required_xp(self.level)
            print(f"Leveled up to {self.level}! Next level requires {self.required_xp} XP.")
        else:
            # Reached max level
            self.required_xp = float('inf')  # No more leveling up
            print(f"Leveled up to max level ({self.max_level})! Excess XP: {self.current_xp}")

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
