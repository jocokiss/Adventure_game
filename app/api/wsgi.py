import sys
from pathlib import Path

# Add the project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.api import create_app

application = create_app()
