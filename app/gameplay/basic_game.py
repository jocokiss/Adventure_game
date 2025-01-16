import pygame

from app.gameplay.config import Config
from app.gameplay.map import Map
from app.gameplay.movement import MovementHandler
from app.gameplay.menu import Menu

from app.sprites.characters.player_sprite import PlayerSprite
from app.sprites.npc.npc_sprites import NPCSprite


class BasicGame:
    def __init__(self):
        self.config = Config()
        self.character = PlayerSprite(self.config)

        self.npc = npc = NPCSprite(self.config, initial_position=(19, 17))
        self.npc.patrol_path = []
        self.npc.is_random_movement = False  # Enable patrolling

        self.movement = MovementHandler(self.config, self.character)
        self.map = Map(self.config)

        self.map.add_npc(npc)

        self.menu = Menu(self.config)

        # Game States
        self.state = "MENU"  # Possible states: MENU, GAME, PAUSE, EXIT
        self.running = True

    def run(self):
        while self.running:
            if self.state == "MENU":
                self.__run_menu()
            elif self.state == "GAME":
                self.__run_game()
            elif self.state == "COMBAT":
                self.__run_combat()
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

    def __run_combat(self):
        """Combat loop."""
        combat_running = True
        while combat_running:
            self.config.dt = pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "EXIT"
                    combat_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "GAME"
                        combat_running = False

            # Draw combat screen
            self.config.screen.fill((0, 0, 0))  # Black background
            self.draw_combat_ui()

            pygame.display.flip()

    def draw_combat_ui(self):
        """Draw the combat UI."""
        # Draw player and enemy health bars
        pygame.draw.rect(self.config.screen, (255, 0, 0), (50, 50, 200, 20))  # Player HP bar
        pygame.draw.rect(self.config.screen, (255, 0, 0), (400, 50, 200, 20))  # NPC HP bar

        # Draw placeholders for the player and NPC
        pygame.draw.rect(self.config.screen, (0, 255, 0), (50, 100, 50, 50))  # Player
        pygame.draw.rect(self.config.screen, (0, 0, 255), (400, 100, 50, 50))  # NPC

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
                            npc.interact(
                                pygame.Vector2(
                                    self.character.coordinate.x,
                                    self.character.coordinate.y
                                )
                            )  # Pass the player's position
                        self.state = "COMBAT"

            keys = pygame.key.get_pressed()

            self.movement.process_movement(keys)
            self.config.calculate_offsets()
            self.map.update_npcs()

            self.map.render_background()

            self.character.update()
            self.character.draw()
            self.map.draw_npcs()

            self.map.render_foreground()

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
