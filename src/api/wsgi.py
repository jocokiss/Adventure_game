from src.api import create_app
import sys

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
