import os

import jwt
import requests
from dotenv import load_dotenv


class GameAPIClient:
    @staticmethod
    def save_game(player_id, data):
        """
        Sends a POST request to save the player's game state.

        Args:
            player_id (str): Unique identifier for the player.
            data (dict): Game state data to save.

        Returns:
            dict: Response from the server.
        """
        url = "https://adventure-game-rl72.onrender.com/save"
        response = requests.post(url, json={"player_id": player_id, **data})
        return response.json()

    @staticmethod
    def load_game(player_id):
        """
        Sends a GET request to load the player's game state.

        Args:
            player_id (str): Unique identifier for the player.

        Returns:
            dict: Response from the server containing the game state.
        """
        url = "https://adventure-game-rl72.onrender.com/load"
        response = requests.get(url, params={"player_id": player_id})
        print(response.json())
        return response.json()

    @staticmethod
    def get_mongo_token():
        """
        Fetch a JWT token containing the MongoDB connection string.

        Returns:
            str: Decoded MongoDB connection string.
        """
        url = "https://adventure-game-rl72.onrender.com/secrets"  # Your Flask API endpoint
        try:
            # Fetch the token from the server
            response = requests.get(url)
            response.raise_for_status()
            token = response.json().get("token")

            # Decode the JWT
            load_dotenv()
            secret_key = os.getenv('TOKEN_KEY')
            decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
            return decoded.get("mongo_uri")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching MongoDB token: {e}")
            return None
        except jwt.ExpiredSignatureError:
            print("Token has expired. Fetch a new one.")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
