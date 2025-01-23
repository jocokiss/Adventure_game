import datetime
import os

import jwt
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


@api.route("/secrets", methods=["GET"])
def get_mongo_token():
    """
    Generate a JWT containing the MongoDB connection string.
    """
    # MongoDB connection string (stored as an environment variable)
    token_key = os.getenv('TOKEN_KEY')
    mongo_uri = os.getenv("MONGO_DB")
    if not mongo_uri:
        return jsonify({"error": "MongoDB connection string not found"}), 404
    if not token_key:
        return jsonify({"error": "Token key not found"}), 404

    try:
        # Generate JWT
        token = jwt.encode(
            {
                "mongo_uri": mongo_uri,  # Add connection string to the token
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),  # Token expiration
            },
            token_key,
            algorithm="HS256",
        )
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": "Failed to generate token", "details": str(e)}), 500
