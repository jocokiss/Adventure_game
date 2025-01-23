import os

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)


# Example route to save game data
@api.route("/save", methods=["POST"])
def save_game():
    data = request.json
    print(f"Saving game data: {data}")
    return jsonify({"status": "success", "message": "Game data saved!"})


# Example route to load game data
@api.route("/load", methods=["GET"])
def load_game():
    player_id = request.args.get("player_id")
    print(f"Loading game data for player_id: {player_id}")
    # Mock data
    data = {"player_id": player_id, "level": 10, "xp": 500}
    return jsonify(data)


@api.route("/mongo", methods=["GET"])
def get_mongo_conn_string():
    """
    Return the MongoDB connection string from the server environment variables.
    """
    if mongo_uri := os.getenv("MONGO"):
        return jsonify({"mongo_uri": mongo_uri})
    return jsonify({"error": "MongoDB connection string not found"}), 404
