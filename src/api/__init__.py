from flask import Flask
from src.api.routes import api  # Adjust the import based on your structure


def create_app():
    application = Flask(__name__)
    application.register_blueprint(api)  # Register your routes
    return application
