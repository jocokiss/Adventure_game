import pygame
import sys


class Menu:
    def __init__(self, config):
        self.screen = config.screen
        self.font = pygame.font.Font(None, 36)
        self.options = []
        self.selected = 0  # Tracks the currently selected option

    def set_options(self, options):
        """Set menu options dynamically."""
        self.options = options
        self.selected = 0  # Reset selection

    def render(self, title):
        """Render the menu options on the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Display Menu Title
        title_text = self.font.render(title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(title_text, title_rect)

        # Calculate start position for menu options
        option_start_y = screen_height // 2 - (len(self.options) * 30) // 2

        # Display Options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (150, 150, 150)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, option_start_y + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_input(self):
        """Handle menu navigation and selection."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    return self.options[self.selected]