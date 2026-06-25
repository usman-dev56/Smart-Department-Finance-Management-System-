# main.py
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.app import SDFFMSApp

if __name__ == "__main__":
    app = SDFFMSApp()
    app.run()