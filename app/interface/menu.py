from app.classes.player import Player
from app.classes.Rouge.rouge_class import Rouge
import json

playable_characters = {
        "Warrior": Player,
        "Rouge": Rouge
    }

class SaveGameNotFound(Exception):
    pass


def main_menu():
    while True:
        new_or_load = int(input("1: NEW GAME\n"
                                "2: LOAD GAME\n"
                                "Your input: "))
        if new_or_load in [1, 2]:
            if new_or_load == 1:
                new_character = character_creation()
            else:
                new_character = load_game()
            return new_character
        else:
            print("Not a valid option")

def load_game():
    while True:
        char_name = input("What is your character's name?: ").lower().capitalize()
        if not char_name or not isinstance(char_name, str):
            print("invalid input")

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


def character_creation():
    while True:
        c_class = input("Which class do you choose?: ").lower()
        if c_class.capitalize() in playable_characters:
            cls = playable_characters[c_class]()
            cls.set_name()
            cls.set_sex()
            return cls

if __name__ == '__main__':
    main_menu()