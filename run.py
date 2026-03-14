#!/usr/bin/env python3
"""
run.py – Launcher that ensures virtual environment and dependencies are ready.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.absolute()
VENV_DIR = PROJECT_DIR / ".env"
VENV_PYTHON = VENV_DIR / ("Scripts" if platform.system() == "Windows" else "bin") / "python"

def is_in_venv():
    """Check if we are already inside a virtual environment."""
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def activate_and_run():
    """If not in venv, re‑execute this script using the venv python."""
    if not is_in_venv():
        if not VENV_PYTHON.exists():
            print("Virtual environment not found. Running setup.py to install dependencies...")
            subprocess.check_call([sys.executable, "setup.py"])
        # Now run the CLI using the venv python
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), __file__] + sys.argv[1:])
    else:
        # We are inside the venv, run the CLI
        from cli import main
        main()

if __name__ == "__main__":
    activate_and_run()