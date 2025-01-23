import requests


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
    def mongo_string():
        """
        Fetch the MongoDB connection string from the server.

        Returns:
            dict: A dictionary containing the MongoDB connection string.
        """
        url = "https://adventure-game-rl72.onrender.com/mongo"  # Your server's route
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching MongoDB connection string: {e}")
            return None
