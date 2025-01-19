import random
import sys

import pygame

from app.characters.non_playable.tree_trunk import TreeTrunk
from app.characters.playable.rogue import Rogue

from app.gameplay.config import Config
from app.gameplay.game_ui import GameUI
from app.gameplay.map.map import Map
from app.gameplay.movement import MovementHandler
from app.gameplay.menu import Menu


class BasicGame:
    def __init__(self):
        self.config = Config()

        self.player = Rogue(self.config)
        self.npc = npc = TreeTrunk(self.config, initial_position=(19, 17))

        self.npc.patrol_path = []
        self.npc.is_random_movement = False  # Enable patrolling

        self.ui = GameUI(self.config)

        self.movement = MovementHandler(self.config, self.player)
        self.map = Map(self.config)

        self.map.add_npc(npc)

        self.menu = Menu(self.config)

        # Game States
        self.state = "MENU"  # Possible states: MENU, GAME, PAUSE, EXIT
        self.running = True

        self.player_turn = None

    def run(self):
        while self.running:
            if self.state == "MENU":
                self.__run_menu()
            elif self.state == "GAME":
                self.__run_game()
            elif self.state == "COMBAT":
                self.__run_combat(self.npc)     # TODO: find the npc near the player
            elif self.state == "PAUSE":
                self.__run_pause()

    def __run_menu(self):
        """Main Menu State."""
        self.menu.set_options(["New Game", "Load Game", "Exit"])

        # Isolate Menu Loop
        while self.state == "MENU":
            self.config.screen.fill((0, 0, 0))  # Clear the screen
            choice = self.menu.handle_input()
            self.menu.render("Main Menu")
            pygame.display.flip()

            if choice == "New Game":
                self.state = "GAME"
            elif choice == "Load Game":
                print("Load Game - Placeholder for save file loading")
                self.state = "GAME"
            elif choice == "Exit":
                self.running = False
                self.state = "EXIT"

    def __run_pause(self):
        """Pause Menu State."""
        self.menu.set_options(["Continue", "Quit to Main Menu", "Exit Game"])

        while self.state == "PAUSE":
            # Render semi-transparent overlay
            # TODO: This is not semi transparent
            overlay = pygame.Surface(self.config.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Black with 180 alpha for transparency
            self.config.screen.blit(overlay, (0, 0))

            # Render the menu
            choice = self.menu.handle_input()
            self.menu.render("Paused")
            pygame.display.flip()

            if choice == "Continue":
                self.state = "GAME"
            elif choice == "Quit to Main Menu":
                self.state = "RESTART"
                self.running = False  # Exit the game loop to restart
            elif choice == "Exit Game":
                self.state = "EXIT"
                self.running = False

    def __run_combat(self, npc):
        """Run the combat loop."""
        self.combat_active = True  # Explicit variable for combat state

        while self.combat_active:

            # Check for player or NPC defeat
            if self.player.combat.health <= 0:
                self.combat_active = False  # End combat
                break  # Explicitly break the loop
            elif npc.combat.health <= 0:
                self.combat_active = False  # End combat
                break  # Explicitly break the loop

            # Handle player and NPC turns
            if self.player_turn:
                self.handle_player_turn(npc)
            else:
                self.handle_npc_turn(npc)

            # Draw combat UI
            self.draw_combat_ui(npc)
            pygame.display.flip()

        self.state = "GAME"

    def handle_player_turn(self, npc):
        """Handle the player's turn."""
        action_taken = False
        skill_keys = {pygame.K_1 + i: i for i in range(len(self.player.combat.skills))}

        while not action_taken:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Check if the pressed key corresponds to a skill
                    if event.key in skill_keys:
                        skill_index = skill_keys[event.key]
                        skill = self.player.combat.skills[skill_index]
                        if skill.use(self.player.combat, npc.combat):  # Use skill on NPC
                            action_taken = True
                            self.player_turn = False  # End player's turn

    def handle_npc_turn(self, npc):
        """Handle the NPC's turn."""
        # NPC performs an action (e.g., attack)
        if npc.combat.skills:
            skill = random.choice(npc.combat.skills)
            # if skill.use(npc.combat, self.player.combat):
            #     print(f"{npc.name} used {skill.name}!")
        else:
            # Default attack if no skills are defined
            self.player.combat.take_damage(10)

        # End NPC's turn
        self.player_turn = True

    def draw_combat_ui(self, npc):
        """Draw the combat UI."""
        self.config.screen.fill((0, 0, 0))  # Black background

        # Display Player and NPC Health
        font = pygame.font.Font(None, 36)
        player_health_text = font.render(f"Player HP: {self.player.combat.health}", True, (255, 255, 255))
        npc_health_text = font.render(f"{npc.name} HP: {npc.combat.health}", True, (255, 255, 255))

        self.config.screen.blit(player_health_text, (50, 50))
        self.config.screen.blit(npc_health_text, (50, 100))

        # Optionally, show skills on the UI
        skill_menu_y = 200
        for index, skill in enumerate(self.player.combat.skills):
            skill_text = font.render(f"{index + 1}: {skill.name}", True, (255, 255, 255))
            self.config.screen.blit(skill_text, (50, skill_menu_y))
            skill_menu_y += 40

    def display_skill_menu(self):
        """Display the skill menu and handle player input."""
        keys = pygame.key.get_pressed()
        for index in range(len(self.player.combat.skills)):
            # Map skill keys to numbers (e.g., 1, 2, 3)
            if keys[pygame.K_1 + index]:  # Adjust for number keys
                return index
        return None

    def __run_game(self):
        """Game State."""
        while self.state == "GAME":
            self.config.dt = pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "EXIT"
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "PAUSE"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:  # Example: 'E' key for interaction
                        for npc in self.map.npcs:  # Iterate through all NPCs on the map
                            npc.sprite.interact(
                                pygame.Vector2(
                                    self.player.sprite.coordinate.x,
                                    self.player.sprite.coordinate.y
                                )
                            )  # Pass the player's position
                        self.state = "COMBAT"

            keys = pygame.key.get_pressed()

            self.movement.process_movement(keys)
            self.config.calculate_offsets()
            self.map.update_npcs()

            self.map.render_background()

            self.player.sprite.update()
            self.player.sprite.draw()
            self.map.draw_npcs()

            self.map.render_foreground()

            self.ui.draw()

            pygame.display.flip()


if __name__ == "__main__":
    while True:
        pipeline = BasicGame()
        pipeline.run()

        if pipeline.state == "EXIT":
            print("Exiting the game...")
            break
        elif pipeline.state == "RESTART":
            print("Restarting the game...")
            continue
