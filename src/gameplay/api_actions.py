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
        url = "http://127.0.0.1:5000/save"
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
        url = "http://127.0.0.1:5000/load"
        response = requests.get(url, params={"player_id": player_id})
        return response.json()
