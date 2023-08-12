import json

import pygame

from app.interface.menu import playable_characters

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Adventure Game")
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):
        self.running = True
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Update game state
        pass

    def render(self):
        # Render graphics
        pass


pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Set up the font
font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    rendered_text = font.render(text, True, (255, 255, 255))
    screen.blit(rendered_text, (x, y))

def main_menu():
    while True:
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the menu options
        draw_text("1: NEW GAME", 100, 200)
        draw_text("2: LOAD GAME", 100, 250)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_character = character_creation()
                    return new_character
                elif event.key == pygame.K_2:
                    new_character = load_game()
                    return new_character

def load_game():
    input_text = ""  # Initialize input_text variable
    while True:
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the input prompt
        draw_text("What is your character's name?: " + input_text, 100, 200)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    char_name = input_text.strip().lower().capitalize()
                    if not char_name or not isinstance(char_name, str):
                        print("Invalid input")
                        continue

                    try:
                        saved_game = f"/Users/jocokiss/Documents" \
                                       f"/adventure_game_project/app" \
                                       f"/saved_games/{char_name}.json"
                        with open(saved_game, 'r') as file:
                            class_attributes = json.load(file)
                    except FileNotFoundError:
                        print("No saved game found")
                        continue

                    cls = playable_characters[class_attributes["class"]]()
                    cls.name = char_name
                    return cls
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

def character_creation():
    input_text = ""  # Initialize input_text variable
    while True:
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the input prompt
        draw_text("Which class do you choose?: " + input_text, 100, 200)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    c_class = input_text.strip().lower().capitalize()
                    if c_class.capitalize() in playable_characters:
                        cls = playable_characters[c_class]()
                        cls.set_name()
                        cls.set_sex()
                        return cls
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# Start the main menu
new_character = main_menu()
