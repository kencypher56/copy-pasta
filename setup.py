"""
setup.py – Automatic dependency installer that always creates a virtual environment.
"""

import subprocess
import sys
import os
from pathlib import Path

REQUIREMENTS_FILE = Path(__file__).parent / "requirements.txt"
VENV_DIR = Path(__file__).parent / ".env"

def install_dependencies():
    """Create a virtual environment (if missing) and install dependencies there."""
    if not VENV_DIR.exists():
        print(f"Creating virtual environment in {VENV_DIR}...")
        import venv
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("Virtual environment already exists.")

    # Determine path to pip in venv
    if sys.platform == "win32":
        pip_path = VENV_DIR / "Scripts" / "pip"
    else:
        pip_path = VENV_DIR / "bin" / "pip"

    print("Installing requirements...")
    subprocess.check_call([str(pip_path), "install", "-r", str(REQUIREMENTS_FILE)])
    print("Dependencies installed successfully in virtual environment.")

if __name__ == "__main__":
    install_dependencies()