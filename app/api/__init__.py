from flask import Flask
from app.api.routes import api  # Adjust the import based on your structure


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)  # Register your routes
    return app
