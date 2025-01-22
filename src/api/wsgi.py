from src.api import create_app
import sys

print("PYTHON PATH:", sys.path)

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
